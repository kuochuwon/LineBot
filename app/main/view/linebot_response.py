from app.main.service import ret
import json
from app.main.constant import LineConstant


def check_line_user(payload) -> None:
    temp = payload.get("events")[0]
    msg_text = temp["message"]["text"]
    user_id = temp["source"]["userId"]
    user_info = {user_id: {"nickname": msg_text}}
    with open("user_info.json", "r", encoding="utf-8") as json_file:
        content = json.load(json_file)
    invitation_url = None
    if content.get(user_id) is None:
        update_line_user(content, user_info)
        invitation_url = (f"https://notify-bot.line.me/oauth/authorize?response_type=code&scope=notify&"
                          f"response_mode=form_post&client_id={LineConstant.NOTIFY.get('CLIENT_ID')}"
                          f"&redirect_uri={LineConstant.NOTIFY.get('local_URI')}"
                          f"&state=f094a459-1d16-42d6-a709-c2b61ec53d60")
        return invitation_url


def update_line_user(content, user_info) -> None:
    with open("user_info.json", "w", encoding="utf-8") as json_file:
        content.update(user_info)
        json.dump(content, json_file, ensure_ascii=False, indent=4)
