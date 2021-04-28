import json
import requests as urllib_requests
from pathlib import Path
from app.main.constant import LineConstant
from app.main.log import logger
from app.main.model.bible import Bible
from app.main.service.line_tools import general_flex_reply, general_reply


def get_general_carousel(filename) -> list:
    with open((Path.cwd() / "flex_message_box/" / filename), 'r', encoding="utf-8") as r:
        expect = json.load(r)
    return expect


# TODO 產生輪播內容
def sending_church_carousel_by_reply(replytoken):
    try:
        flex_message = get_general_carousel("church_homepage.json")
        general_reply(replytoken, flex_message)
        # json_for_msg = dict(
        #     replyToken=replytoken,
        #     messages=flex_message
        # )
        # result = urllib_requests.post(
        #     LineConstant.OFFICIAL_REPLY_API,
        #     headers=LineConstant.push_header,
        #     json=json_for_msg)  # HINT must use json as parameter
        # logger.debug(f"http status: {result.status_code}")
        # logger.debug(f"http hint: {result.text}")
    except Exception as e:
        logger.exception(f"sending carousel failed {e}")


def sending_tutorial(replytoken):
    pic_1 = "https://i.imgur.com/nYq2Aud.png"
    pic_2 = "https://i.imgur.com/SutrRum.png"
    tutorial_1 = {
        "type": "image",
        "originalContentUrl": pic_1,
        "previewImageUrl": pic_1
    }
    tutorial_2 = {
        "type": "image",
        "originalContentUrl": pic_2,
        "previewImageUrl": pic_2
    }
    # replyMsg = {
    #     "type": "text",
    #     "text": "Hello"
    # }
    general_reply(replytoken, [tutorial_1, tutorial_2])
    logger.debug("觸發教學流程")


def sending_bible_sentence(replytoken):
    flex_message = get_general_carousel("daily_bibile.json")
    # sentence = flex_message["body"]["contents"][0]["contents"][0]["contents"][0]["text"]
    # locate = flex_message["body"]["contents"][0]["contents"][1]["contents"][0]["text"]
    bible: Bible = Bible.get_by_random()
    flex_message[0]["contents"]["body"]["contents"][0]["contents"][0]["contents"][0]["text"] = bible.sentence
    flex_message[0]["contents"]["body"]["contents"][0]["contents"][1]["contents"][0]["text"] = bible.locate
    general_reply(replytoken, flex_message)
    # general_flex_reply(replytoken, flex_message)
    logger.debug("觸發讀經")
