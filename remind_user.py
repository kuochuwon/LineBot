import datetime
import os

from dotenv import load_dotenv
base_dir = os.path.abspath(os.path.dirname(__file__))  # noqa 為了在import app.main以前將環境變數載入，main/init裡面有config會呼叫到.env
dotenv_path = os.path.join(base_dir, ".env")  # noqa
load_dotenv(dotenv_path=dotenv_path)  # noqa

from app.main import create_app
from app.main.model.task import sdTask


app = create_app(os.getenv("FLASK_CONFIG") or "development")


def get_next_monday():
    # HINT ref: https://stackoverflow.com/questions/8801084/how-to-calculate-next-friday/8801540
    today = datetime.date.today()
    sunday = today + datetime.timedelta((6-today.weekday()) % 7)
    return sunday


def reminder_content(result: list):
    content = dict()
    for row in result:  # 將負責人的姓名當成key，以免當同一人有多個事工，訊息的整理會太亂
        content.setdefault(row.name, []).append(row.task)

    msg = "下週服事名單如下: \n"
    for name, tasks in content.items():
        task_msg = ""
        for task in tasks:
            task_msg += f"{task} "
        msg += f"{name} {task_msg}\n"

    print(msg)
    return content


def main():
    with app.app_context():
        target_day = get_next_monday()
        result = sdTask.get_by_time(target_day, target_day)
        content = reminder_content(result)
        a = "temp"


if __name__ == "__main__":
    main()
