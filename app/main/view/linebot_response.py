from app.main.model.task import sdTask
from pathlib import Path
import json
import platform
import os
import requests as urllib_requests
from app.main import db
from app.main.constant import LineConstant
from app.main.model.user import sdUser
from app.main.service.word_docx_processor import WordParser, PostProcess
from app.main.log import logger
from app.main.service.line_flex_message import sending_carousel_by_reply, sending_tutorial, sending_joke

func_dict = {
    "1": sending_carousel_by_reply,
    "2": sending_tutorial,
    "3": sending_joke
}


def notify_handler(payload):
    try:
        name = payload.get("name")
        text = payload.get("text")
        search_res = sdUser.search_by_name(name)
        user_notify_token = search_res.access_token

        response = {"hint": "已接收請求，但內容為空"}
        json_for_msg = dict(
            message=text,  # HINT 注意這裡跟line push API的messages不一樣
            stickerPackageId=446,
            stickerId=1988
        )
        header = LineConstant.notify_header
        header.update({"Authorization": f"Bearer {user_notify_token}"})
        result = urllib_requests.post(
            LineConstant.OFFICIAL_NOTIFY_API,
            headers=header,
            data=json_for_msg)  # HINT must use data as parameter
        if result.status_code == 200:
            response = {"hint": "訊息發送成功"}
        return response
    except Exception as e:
        # print(f"notify failed: {e}")
        logger.exception(f"notify failed: {e}")
        raise


def check_line_user(user_id, msg_text, replytoken):
    invitation_url = ""
    search_res = sdUser.search(user_id)
    if search_res is None:
        add_line_user_to_db(search_res, msg_text, user_id)
        invitation_url = generate_url(user_id)
    return invitation_url, replytoken


# TODO 進行例外處理
def message_preprocess(payload) -> str:
    temp = payload.get("events")[0]
    replytoken = temp["replyToken"]
    msg_text = temp["message"]["text"]  # HINT name
    user_id = temp["source"]["userId"]
    return user_id, msg_text, replytoken


def match_keyword(msg_text):
    return LineConstant.RESPONSE_CODE.get(msg_text)


def general_sticker(package_id, sticker_id):
    return {"type": "sticker", "packageId": package_id, "stickerId": sticker_id}


def general_text(text: str):
    return {"type": "text", "text": text}


def general_replyer(replytoken, msg, sticker=None):
    try:
        json_for_msg = dict(
            replyToken=replytoken,
            messages=[msg, sticker] if sticker else msg
        )
        # print(f"json_for_msg: {json_for_msg}")
        logger.debug(f"json_for_msg: {json_for_msg}")
        result = urllib_requests.post(
            LineConstant.OFFICIAL_REPLY_API,
            headers=LineConstant.push_header,
            json=json_for_msg)  # HINT must use json as parameter
        logger.debug(f"http code: {result.status_code}, http text: {result.text}")
        return result
    except Exception as e:
        logger.exception(f"reply failed: {e}")
        raise


def text_handler(payload) -> dict:
    user_id, msg_text, replytoken = message_preprocess(payload)

    # HINT: 使用match_keyword限制會傳入func_dict的參數，
    # 如果是None就不會呼叫func_dict，
    # 以免發生:TypeError: 'NoneType' object is not callable錯誤，有空找方法優化
    resp_code = match_keyword(msg_text)
    if resp_code:
        func_dict.get(resp_code)(replytoken)
        msg = general_text("This is Flex message")

    elif msg_text[:4] == "服事提醒":
        user_name = msg_text.split(" ")[1]
        invitation_url, replytoken = check_line_user(user_id, user_name, replytoken)
        logger.debug(f"reply token: {replytoken}")
        if invitation_url:
            text = (f"平安，已經將您的資料建檔，為了進一步確保服務品質，建議您點選以下連結註冊備援小幫手"
                    f"連結: {invitation_url}")
            msg = general_text(text)
        else:
            text = (f"平安，您的資料已建檔，若下週輪到您服事，我會事先通知您~\n"
                    f"敬請期待未來更多功能上線。")
            msg = general_text(text)
        sticker = general_sticker(446, 1989)
        result = general_replyer(replytoken, msg, sticker)
        logger.debug(f"reply status code: {result.status_code}")

    else:
        text = "已收到訊息。"
        msg = general_text(text)
        result = general_replyer(replytoken, msg)
        logger.debug(f"reply status code: {result.status_code}")
    return msg


def download_line_content(file_id, file_name):
    env = os.getenv("FLASK_CONFIG")
    if env == "heroku":
        with urllib_requests.get(
                LineConstant.OFFICIAL_CONTENT_API.replace("<file_id>", file_id),
                headers=LineConstant.push_header,
                stream=True) as r:
            r.raise_for_status()
            with open((Path.cwd() / "downloads/" / file_name), 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    # link1: https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests # noqa
                    # link2: https://stackoverflow.com/questions/19602931/basic-http-file-downloading-and-saving-to-disk-in-python # noqa
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk:
                    f.write(chunk)
        print(f"file saved successfully: {file_name}, id: {file_id}")
        logger.debug(f"file saved successfully: {file_name}, id: {file_id}")
    else:
        print("download canceled because of local testing environment.")
        logger.debug("download canceled because of local testing environment.")


def delete_duplicate_before_inserting(member_duties: dict):
    dates = list(member_duties.keys())
    dates.sort()
    sdTask.delete_by_date(dates[0], dates[-1])
    db.session.commit()


def insert_duties_db(member_duties: dict):
    try:
        delete_duplicate_before_inserting(member_duties)
        for date, value in member_duties.items():
            for name, tasks in value.items():
                for task in tasks:
                    obj = sdTask.add(name, date, task)
                    db.session.add(obj)
        db.session.commit()
    except Exception as e:
        print(f"duties insert failed: {e}")
        db.session.rollback()
        raise
    finally:
        db.session.close()


def file_handler(payload):
    temp = payload.get("events")[0]
    replytoken = temp["replyToken"]
    file_id = temp["message"]["id"]  # HINT name
    file_name = temp["message"]["fileName"]

    download_line_content(file_id, file_name)
    wp = WordParser(file_name)
    pp = PostProcess()
    member_duties = wp.parsing_church_schedule()
    check_result, conflict_flag = pp.check_conflict(member_duties)
    if conflict_flag == 0:
        insert_duties_db(member_duties)

    logger.debug(f"check result: {check_result}")

    msg = general_text(check_result)
    sticker = general_sticker(446, 1989)
    result = general_replyer(replytoken, msg, sticker)
    logger.debug(f"reply status code: {result.status_code}")
    return msg


def generate_url(user_id: str):
    invitation_url = (f"https://notify-bot.line.me/oauth/authorize?response_type=code&scope=notify&"
                      f"response_mode=form_post&client_id={LineConstant.NOTIFY.get('CLIENT_ID')}"
                      f"&redirect_uri={LineConstant.NOTIFY.get(platform.system())}"
                      f"&state={user_id}")
    return invitation_url


def add_line_user_to_db(search_res, msg_text, user_id):
    if search_res is None:
        try:
            obj = sdUser().add(msg_text, user_id)
            db.session.add(obj)
            db.session.commit()
        except Exception as e:
            # print((f"failed to update data to SQL: {str(e)}"))
            logger.exception(f"failed to update data to SQL: {str(e)}")
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
    logger.debug(f"Notify code is {code}")

    # HINT magic method, 從網路上抄的，還不確定是否一定要這樣寫 https://stackoverflow.com/questions/20759981/python-trying-to-post-form-using-requests by atupal # noqa
    session = urllib_requests.Session()
    result = session.post(
        LineConstant.OFFICIAL_OAUTH_API,
        headers={'User-Agent': 'Mozilla/5.0'},
        params=files
    )
    output = json.loads(result.text)
    logger.debug(f"Notify output is {output}")
    access_token = output.get("access_token")
    try:
        obj = sdUser().update(user_id, access_token)
        db.session.add(obj)
        db.session.commit()

    except Exception as e:
        logger.exception(f"failed to update user: {e}")
    finally:
        db.session.close()


def webhook_message_checker(payload):
    try:
        if payload.get("events"):
            temp = payload.get("events")[0]
            if temp["message"]["type"] == "text":
                print("------ type is text ------")
                logger.debug("------ type is text ------")
                return "text"
            elif temp["message"]["type"] == "image":
                print("------ type is image ------")
                logger.debug("------ type is image ------")
                return "image"
            elif temp["message"]["type"] == "file":
                print("------ type is file ------")
                logger.debug("------ type is file ------")
                return "file"
            else:
                print("------ type is unknown ------")
                logger.debug("------ type is unknown ------")
                return False
        else:
            return False
    except Exception as e:
        logger.exception(f"invalid payload: {e}")
        return False
