from test.base import BaseTestCase2
from app.main.service.line_flex_message import get_general_carousel, get_tutorial

first_layer_keyword = {"type", "hero", "body", "size", "footer"}  # set


class TestMainFunction(BaseTestCase2):
    def test_church_carousel(self):
        # keyword_set = {"type", "hero", "body", "size", "footer"}  # set
        for_checking = get_general_carousel("church_homepage.json").get("contents")
        carousel_objs = for_checking.get("contents")
        for each in carousel_objs:
            boo_res = set(each.keys()).issubset(first_layer_keyword)  # HINT check each key is valid or not
            self.assertTrue(boo_res)
        # self.check_first_layer(carousel_objs)

    def test_bible_sentence(self):
        for_checking = get_general_carousel("daily_bibile.json").get("contents")
        boo_res = set(for_checking.keys()).issubset(first_layer_keyword)
        self.assertTrue(boo_res)

    def test_tutorial_page(self):
        image_set = ["type", "originalContentUrl", "previewImageUrl"]
        for_checking1, for_checking2 = get_tutorial()
        boo_res1 = set(for_checking1.keys()).issubset(image_set)
        boo_res2 = set(for_checking2.keys()).issubset(image_set)
        self.assertTrue(boo_res1)
        self.assertTrue(boo_res2)
