import requests as urllib_requests
from app.main.constant import LineConstant
from app.main.log import logger


# def general_reply(replytoken, identifier, msgs: list):
#     try:
#         # HINT 使用者須了解調用此函式時，msgs須為list
#         json_for_msg = dict(
#             replyToken=replytoken,
#             messages=msgs
#         )
#         result = urllib_requests.post(
#             LineConstant.OFFICIAL_REPLY_API,
#             headers=LineConstant().generate_push_or_reply_header(identifier),
#             json=json_for_msg)  # HINT must use json as parameter
#         logger.debug(f"http status: {result.status_code}")
#         logger.debug(f"http hint: {result.text}")
#     except Exception as e:
#         logger.exception(f"sending reply failed {e}")
#         raise


def general_replyer(replytoken, identifier, *args):
    # HINT *args include msgs and stickers
    try:
        json_for_msg = dict(
            replyToken=replytoken,
            messages=[*args]
            # messages=[msg, sticker] if sticker else [msg]
        )
        logger.debug(f"json_for_msg: {json_for_msg}")
        result = urllib_requests.post(
            LineConstant.OFFICIAL_REPLY_API,
            headers=LineConstant().generate_push_or_reply_header(identifier),
            json=json_for_msg)  # HINT must use json as parameter
        logger.debug(f"http status: {result.status_code}")
        logger.debug(f"http hint: {result.text}")
        return result
    except Exception as e:
        logger.exception(f"reply failed: {e}")
        raise
