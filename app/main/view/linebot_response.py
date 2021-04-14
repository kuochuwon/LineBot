from os import access
from app.main.service import ret
import json
from app.main.constant import LineConstant
import requests as urllib_requests
import platform


def check_line_user(payload) -> None:
    temp = payload.get("events")[0]
    msg_text = temp["message"]["text"]
    user_id = temp["source"]["userId"]
    user_info = {user_id: {"nickname": msg_text}}
    with open("user_info.json", "r", encoding="utf-8") as json_file:
        content = json.load(json_file)
    invitation_url = (f"https://notify-bot.line.me/oauth/authorize?response_type=code&scope=notify&"
                      f"response_mode=form_post&client_id={LineConstant.NOTIFY.get('CLIENT_ID')}"
                      f"&redirect_uri={LineConstant.NOTIFY.get('local_URI')}"
                      f"&state={user_id}")
    if content.get(user_id) is None:
        update_line_user(content, user_info)
    return invitation_url


def update_line_user(content, user_info) -> None:
    with open("user_info.json", "w", encoding="utf-8") as json_file:
        print("new user")
        content.update(user_info)
        json.dump(content, json_file, ensure_ascii=False, indent=4)


def append_notify_token(user_id: str, access_token: str) -> None:
    with open("user_info.json", "r", encoding="utf-8") as json_file:
        content = json.load(json_file)
    with open("user_info.json", "w", encoding="utf-8") as json_file:
        print("---------")
        print("user_id: ", content.get(user_id))
        print(f"access_token: {access_token}")
        print("---------")
        content[user_id]["access_token"] = access_token
        json.dump(content, json_file, ensure_ascii=False, indent=4)


def retrieve_notify_token_from_callback(request):
    code = request.form.get('code')
    user_id = request.form.get('state')  # 我將state故意設定為資料庫中對應的user_id，用來統整messaging API and Notify的使用者
    files = {
        "grant_type": "authorization_code",
        "client_id": LineConstant.NOTIFY.get('CLIENT_ID'),
        "client_secret": LineConstant.NOTIFY.get('SECRET'),
        "code": code
    }
    if platform.system() == "Windows":
        files.update({"redirect_uri": LineConstant.NOTIFY.get('local_URI')})
    else:  # Linux
        files.update({"redirect_uri": LineConstant.NOTIFY.get('remote_URI')})
    print("------------")
    print("code",  code)  # for debug
    print("------------")

    # HINT magic method, 從網路上抄的，還不確定是否一定要這樣寫 https://stackoverflow.com/questions/20759981/python-trying-to-post-form-using-requests by atupal#
    session = urllib_requests.Session()
    result = session.post(
        LineConstant.OFFICIAL_OAUTH_API,
        headers={'User-Agent': 'Mozilla/5.0'},
        params=files
    )
    output = json.loads(result.text)
    print("------------")
    print(f"output: {output}")
    print("------------")
    access_token = output.get("access_token")
    append_notify_token(user_id, access_token)
