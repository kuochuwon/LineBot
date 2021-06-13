import datetime
import requests as urllib_requests
import os
import platform

from dotenv import load_dotenv
base_dir = os.path.abspath(os.path.dirname(__file__))  # noqa 為了在import app.main以前將環境變數載入，main/init裡面有config會呼叫到.env
dotenv_path = os.path.join(base_dir, ".env")  # noqa
load_dotenv(dotenv_path=dotenv_path)  # noqa

from app.main import create_app
from app.main.model.task import sdTask
from app.main.model.user import sdUser
from app.main.constant import LineConstant
from app.main.log import logger

app = create_app(os.getenv("FLASK_CONFIG") or "development")


def is_monday():
    weekday = datetime.date.today().weekday()
    if weekday == 0:
        return True
    else:
        print(f"Today's weekday is {weekday}, (0 is Monday), not Monday.")
        return False


def get_next_sunday():
    # HINT ref: https://stackoverflow.com/questions/8801084/how-to-calculate-next-friday/8801540
    today = datetime.date.today()
    sunday = today + datetime.timedelta((6-today.weekday()) % 7)
    return sunday


def reminder_content(user_result: list, users: list):
    content = dict()
    user_id_pool = dict()
    user_access_token_pool = dict()
    for user in users:
        user_id_pool.update({user.name: user.user_unique_id})
        user_access_token_pool.update({user.name: user.access_token})

    for row in user_result:  # 將負責人的姓名當成key，以免當同一人有多個事工，訊息的整理會太亂
        content.setdefault(row.name, []).append(row.task)

    msg = "下週服事名單如下: \n"
    for name, tasks in content.items():
        name = "郭超望" if name == "郭超立" else name  # HINT for debug
        task_msg = ""
        for task in tasks:
            task_msg += f"{task} "
        each_msg = f"{name} {task_msg}\n"
        msg += each_msg
        user_id = user_id_pool.get(name)
        if user_id:
            user_result = urllib_requests.post(
                LineConstant.PUSH.get(platform.system()),
                json={"user_id": user_id, "text": f"服事提醒: {each_msg}"}  # HINT 這邊必須用JSON
            )
            # a = "temp"
            user_result.status_code = 401  # for debug
            if user_result.status_code != 200:  # HINT 當PUSH失敗，改用Notify (request == name)
                user_result = urllib_requests.post(
                    LineConstant.NOTIFY.get(platform.system()),
                    json={"name": name, "text": f"服事提醒: {each_msg}"}
                )
        print(f"each: {each_msg}")

    print("---------------")
    admin_id = user_id_pool.get("郭超望")  # TODO 不要寫死
    user_result = urllib_requests.post(
        LineConstant.PUSH.get(platform.system()),
        json={"user_id": admin_id, "text": f"服事提醒: {msg}"}
    )
    if user_result.status_code != 200:  # HINT 當PUSH失敗，改用Notify (request == name)
        user_result = urllib_requests.post(
            LineConstant.NOTIFY.get(platform.system()),
            json={"name": "郭超望", "text": f"服事提醒: {each_msg}"}  # TODO 不要寫死
        )
    print(msg)


def main():
    with app.app_context():
        flag = is_monday()
        # flag = True  # HINT for debug
        if flag:
            target_day = get_next_sunday()
            users = sdUser.getall()
            result = sdTask.get_by_time(target_day, target_day)
            reminder_content(result, users)


if __name__ == "__main__":
    main()
