from test.base import BaseTestCase
from app.main.view.linebot_response import check_line_user
import re
"""
如果在測試檔案中，加入__init__等沒有test字首的function，vscode會抓不到test framework
"""


class TestAddLineUser(BaseTestCase):
    def test_check_line_user(self):
        users = ["0xabb1230", "false_case"]
        name = ["true_case", "false_case"]
        replys = ["true_token", "false_token"]

        expect = ["", "https://notify-bot.line.me/"]
        test_result = []
        for index in range(2):
            invitation_url, replytoken = check_line_user(users[index], name[index], replys[index])
            test_result.append(invitation_url)
        for index in range(2):
            e = re.match(expect[index], test_result[index])
            self.assertTrue(e)
