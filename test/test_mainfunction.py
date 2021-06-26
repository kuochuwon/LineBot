from test.base import BaseTestCase2
from app.main.service.line_flex_message import get_general_carousel


class TestMainFunction(BaseTestCase2):
    def test_church_carousel(self):
        keyword_set = {"type", "hero", "body", "size", "footer"}  # set
        for_checking = get_general_carousel("church_homepage.json").get("contents")
        carousel_objs = for_checking.get("contents")
        for each in carousel_objs:
            boo_res = set(each.keys()).issubset(keyword_set)  # HINT check each key is valid or not
            self.assertTrue(boo_res)
