import json
import platform

import requests as urllib_requests
from app.main import db
from app.main.constant import LineConstant
from app.main.model.user import sdUser
from app.main.service.word_docx_processor import parsing_church_schedule


def text_handler(payload) -> dict:
    invitation_url, replytoken = check_line_user(payload)
    print(f"reply token: {replytoken}")
    msg = {
        "type": "text",
        "text": f"平安，已經將您的資料建檔，為了進一步確保服務品質，建議您點選以下連結註冊備援小幫手"
        f"連結: {invitation_url}"}

    sticker = {
        "type": "sticker",
        "packageId": "446",
        "stickerId": "1989"
    }

    json_for_msg = dict(
        replyToken=replytoken,
        messages=[msg, sticker]
    )
    print(f"json_for_msg: {json_for_msg}")
    result = urllib_requests.post(
        LineConstant.OFFICIAL_REPLY_API,
        headers=LineConstant.push_header,
        json=json_for_msg)  # HINT must use json as parameter
    print(f"reply status code: {result.status_code}")
    return msg


def file_handler(payload):
    # temp = payload.get("events")[0]
    # replytoken = temp["replyToken"]
    # file_id = temp["message"]["id"]  # HINT name
    # file_name = temp["message"]["fileName"]
    parsing_church_schedule()

    # with urllib_requests.get(
    #         LineConstant.OFFICIAL_CONTENT_API.replace("<file_id>", file_id),
    #         headers=LineConstant.push_header,
    #         stream=True) as r:
    #     r.raise_for_status()
    #     with open((Path.cwd() / "downloads/" / file_name), 'wb') as f:
    #         for chunk in r.iter_content(chunk_size=8192):
    #             # link1: https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests # noqa
    #             # link2: https://stackoverflow.com/questions/19602931/basic-http-file-downloading-and-saving-to-disk-in-python # noqa
    #             # If you have chunk encoded response uncomment if
    #             # and set chunk_size parameter to None.
    #             # if chunk:
    #             f.write(chunk)
    # print(f"file saved successfully: {file_name}, id: {file_id}")


def check_line_user(payload) -> str:
    temp = payload.get("events")[0]
    replytoken = temp["replyToken"]
    msg_text = temp["message"]["text"]  # HINT name
    user_id = temp["source"]["userId"]

    invitation_url = generate_url(user_id)
    search_res = sdUser.search(user_id)
    if search_res is None:
        add_line_user_to_db(search_res, msg_text, user_id)
    return invitation_url, replytoken


def generate_url(user_id: str):
    if platform.system() == "Windows":
        invitation_url = (f"https://notify-bot.line.me/oauth/authorize?response_type=code&scope=notify&"
                          f"response_mode=form_post&client_id={LineConstant.NOTIFY.get('CLIENT_ID')}"
                          f"&redirect_uri={LineConstant.NOTIFY.get('local_URI')}"
                          f"&state={user_id}")
    else:  # Linux
        invitation_url = (f"https://notify-bot.line.me/oauth/authorize?response_type=code&scope=notify&"
                          f"response_mode=form_post&client_id={LineConstant.NOTIFY.get('CLIENT_ID')}"
                          f"&redirect_uri={LineConstant.NOTIFY.get('remote_URI')}"
                          f"&state={user_id}")
    return invitation_url


def add_line_user_to_db(search_res, msg_text, user_id):
    if search_res is None:
        try:
            obj = sdUser().add(msg_text, user_id)
            db.session.add(obj)
            db.session.commit()
        except Exception as e:
            print((f"failed to update data to SQL: {str(e)}"))
            # logger.error(f"failed to update data to SQL: {str(e)}")
            db.session.rollback()
            raise
        finally:
            db.session.close()


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

    # HINT magic method, 從網路上抄的，還不確定是否一定要這樣寫 https://stackoverflow.com/questions/20759981/python-trying-to-post-form-using-requests by atupal # noqa
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
    # append_notify_token(user_id, access_token)
    try:
        obj = sdUser().update(user_id, access_token)
        db.session.add(obj)
        db.session.commit()
    except Exception as e:
        print(f"failed to update user: {e}")


def webhook_message_checker(payload):
    try:
        if payload.get("events"):
            temp = payload.get("events")[0]
            if temp["message"]["type"] == "text":
                print("------ type is text ------")
                return "text"
            elif temp["message"]["type"] == "image":
                print("------ type is image ------")
                return "image"
            elif temp["message"]["type"] == "file":
                print("------ type is file ------")
                return "file"
            else:
                print("------ type is unknown ------")
                return False
        else:
            return False
    except Exception as e:
        print(f"-------invalid payload: {e}-------")
        return False
