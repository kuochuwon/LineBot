import json


def check_line_user(payload) -> None:
    temp = payload.get("events")[0]
    msg_text = temp["message"]["text"]
    user_id = temp["source"]["userId"]
    user_info = {user_id: [msg_text]}
    with open("user_info.json", "r", encoding="utf-8") as json_file:
        content = json.load(json_file)
    if content.get(user_id) is None:
        update_line_user(content, user_info)


def update_line_user(content, user_info) -> None:
    with open("user_info.json", "w", encoding="utf-8") as json_file:
        content.update(user_info)
        json.dump(content, json_file, ensure_ascii=False, indent=4)
