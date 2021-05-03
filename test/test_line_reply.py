from test.base import BaseTestCase2  # HINT: 需經過db的import (line:4)
from app.main.service.line_flex_message import get_general_carousel


class TestLineReply(BaseTestCase2):
    def test_reply_church_msg(self):
        flex_message = get_general_carousel("church_homepage.json")
        flex_keys = list(flex_message.keys())
        expect = {
            "type": "flex",
            "altText": "This is a Flex Message",
            "contents": {
                "type": "carousel",
                "contents": []
            }
        }

        # HINT can be more concise?
        test = {
            flex_keys[0]: flex_message[flex_keys[0]],
            flex_keys[1]: flex_message[flex_keys[1]],
            flex_keys[2]: {"type": flex_message[flex_keys[2]]["type"],
                           "contents": []}
        }

        self.assertIsInstance(flex_message, dict)
        self.assertEqual(expect, test)
        a = "temp"

    def test_reply_bible_msg(self):
        flex_message = get_general_carousel("daily_bibile.json")
        flex_keys = list(flex_message.keys())
        expect = {
            "type": "flex",
            "altText": "This is a Flex Message",
            "contents": {
                "type": "bubble",
                "hero": {}
            }
        }
        # HINT can be more concise?
        test = {
            flex_keys[0]: flex_message[flex_keys[0]],
            flex_keys[1]: flex_message[flex_keys[1]],
            flex_keys[2]: {"type": flex_message[flex_keys[2]]["type"],
                           "hero": {}}
        }
        self.assertIsInstance(flex_message, dict)
        self.assertEqual(expect, test)
