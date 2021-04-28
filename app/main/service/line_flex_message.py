import json
from pathlib import Path

from app.main.log import logger
from app.main.model.bible import Bible
from app.main.service.line_tools import general_reply


def get_general_carousel(filename) -> list:
    with open((Path.cwd() / "flex_message_box/" / filename), 'r', encoding="utf-8") as r:
        expect = json.load(r)
    return expect


# TODO 產生輪播內容
def sending_church_carousel_by_reply(replytoken):
    try:
        flex_message = get_general_carousel("church_homepage.json")
        general_reply(replytoken, flex_message)
    except Exception as e:
        logger.exception(f"sending carousel failed {e}")
        raise


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
    general_reply(replytoken, [tutorial_1, tutorial_2])
    logger.debug("觸發教學流程")


def sending_bible_sentence(replytoken):
    flex_message = get_general_carousel("daily_bibile.json")
    bible: Bible = Bible.get_by_random()
    flex_message[0]["contents"]["body"]["contents"][0]["contents"][0]["contents"][0]["text"] = bible.sentence
    flex_message[0]["contents"]["body"]["contents"][0]["contents"][1]["contents"][0]["text"] = bible.locate
    general_reply(replytoken, flex_message)
    logger.debug("觸發讀經")
