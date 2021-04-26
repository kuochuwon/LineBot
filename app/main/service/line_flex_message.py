import json
import requests as urllib_requests
from pathlib import Path
from app.main.constant import LineConstant
from app.main.log import logger


def carousel_generator() -> list:
    with open((Path.cwd() / "flex_message_box/" / "church_homepage.json"), 'r', encoding="utf-8") as r:
        expect = json.load(r)
    return expect


# TODO 產生輪播內容
def sending_carousel_by_reply(replytoken):
    try:
        msg_list = carousel_generator()
        json_for_msg = dict(
            replyToken=replytoken,
            messages=msg_list
        )
        result = urllib_requests.post(
            LineConstant.OFFICIAL_REPLY_API,
            headers=LineConstant.push_header,
            json=json_for_msg)  # HINT must use json as parameter
        logger.debug("hello carousel")
        logger.debug(f"http status: {result.status_code}")
        logger.debug(f"http hint: {result.text}")
    except Exception as e:
        logger.exception(f"sending carousel failed {e}")


def sending_tutorial(replytoken):
    logger.debug("觸發教學流程")


def sending_joke(replytoken):
    logger.debug("觸發說笑話")
