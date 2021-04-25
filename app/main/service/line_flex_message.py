import json
import requests as urllib_requests
from pathlib import Path
from app.main.constant import LineConstant
from app.main.log import logger


def carousel_generator() -> list:
    with open((Path.cwd() / "backup_info/" / "carousel.json"), 'r', encoding="utf-8") as r:
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
        # return result.status_code
    except Exception as e:
        # logger.exception(f"exception code: {result.status_code}")
        logger.exception(f"sending carousel failed {e}")
    # return result
