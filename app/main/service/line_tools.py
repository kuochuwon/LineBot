import requests as urllib_requests
from app.main.constant import LineConstant
from app.main.log import logger
from typing import List

# TODO 產生輪播內容


def general_flex_reply(replytoken, msg):
    try:
        json_for_msg = dict(
            replyToken=replytoken,
            messages=msg
        )
        result = urllib_requests.post(
            LineConstant.OFFICIAL_REPLY_API,
            headers=LineConstant.push_header,
            json=json_for_msg)  # HINT must use json as parameter
        logger.debug(f"http status: {result.status_code}")
        logger.debug(f"http hint: {result.text}")
    except Exception as e:
        logger.exception(f"sending carousel failed {e}")


# def get_reply_json(replytoken, msgs, mode):
#     json_for_msg = dict(
#         replyToken=replytoken,
#         messages=msgs
#     )
#     return json_for_msg
# def get_reply_json(replytoken, msgs, mode):
#     if mode == 0:  # flex message
#         json_for_msg = dict(
#             replyToken=replytoken,
#             messages=msgs
#         )
#     elif mode == 1:  # simple message
#         json_for_msg = dict(
#             replyToken=replytoken,
#             messages=msgs
#         )
#     return json_for_msg


def general_reply(replytoken, msgs):
    try:
        json_for_msg = dict(
            replyToken=replytoken,
            messages=msgs
        )
        result = urllib_requests.post(
            LineConstant.OFFICIAL_REPLY_API,
            headers=LineConstant.push_header,
            json=json_for_msg)  # HINT must use json as parameter
        logger.debug(f"http status: {result.status_code}")
        logger.debug(f"http hint: {result.text}")
    except Exception as e:
        logger.exception(f"sending carousel failed {e}")
