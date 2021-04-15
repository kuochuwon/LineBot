import requests as urllib_requests
from app.main.constant import LineConstant
from app.main.dto.thelinebot import LineBotDto
from app.main.service import ret
from app.main.util.common import (aaa_verify, api_exception_handler,
                                  check_access_authority)
from app.main.view.linebot_response import (
    check_line_user, excel_handler, retrieve_notify_token_from_callback,
    webhook_message_checker)
from flask import request
from flask_api import status
from flask_restplus import Resource

# from werkzeug.exceptions import NotFound

api = LineBotDto.api
response_status = {status.HTTP_200_OK: ret.get_code_full(ret.RET_OK),
                   status.HTTP_401_UNAUTHORIZED: ret.get_code_full(ret.RET_NO_CUST_ID),
                   status.HTTP_404_NOT_FOUND: ret.get_code_full(ret.RET_NOT_FOUND)}


@api.route("/callback")
class Callback(Resource):
    def post(self):
        """ line bot response """
        retrieve_notify_token_from_callback(request)
        response = None
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK


@api.route("/notify")
class LineNotify(Resource):
    def post(self):
        """ connecting line notify to send free messeage """
        # TODO 改寫成輸入姓名，程式從JSON中尋找對應姓名的notify access token，藉此發送給特定人士
        payload = request.json
        print("------------")
        print(payload)  # for debug
        print("------------")
        response = {"hint": "已接收請求，但內容為空"}
        if payload.get("events"):
            temp = payload.get("events")[0]
            text = temp.get("text")
            json_for_msg = dict(
                message=text  # HINT 注意這裡跟line push API的messages不一樣
            )
            result = urllib_requests.post(
                LineConstant.OFFICIAL_NOTIFY_API,
                headers=LineConstant.notify_header,
                data=json_for_msg)
            if result.status_code == 200:
                response = {"hint": "訊息發送成功"}

        # if payload.get("events"):
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK


@api.route("/push")
class Push(Resource):
    # @api.expect(_header, _get_all_device,
    #             validate=True)
    # @api.doc(responses=response_status)
    # @jwt_required
    # @check_access_authority
    # @api_exception_handler
    def post(self):
        """ connecting line bot API to push messeage """
        payload = request.json

        print("------------")
        print(payload)  # for debug
        print("------------")
        response = {"hint": "已接收請求，但內容為空"}
        if payload.get("events"):
            temp = payload.get("events")[0]
            nickname = temp.get("nickname")
            text = temp.get("text")
            json_for_msg = dict(
                to=LineConstant.user_id.get(nickname),
                messages=[{
                    "type": "text",
                    "text": text
                }]
            )

            result = urllib_requests.post(
                LineConstant.OFFICIAL_PUSH_API,
                headers=LineConstant.push_header,
                json=json_for_msg)
            if result.status_code == 200:
                response = {"hint": "訊息發送成功"}

        # if payload.get("events"):
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK


@api.route("/webhook")
class Webhook(Resource):
    # HINT 技術原理與流程: 使用者向linebot發送訊息，
    # line server收到後會向指定的URI發出一個POST請求，
    # 並包含使用者ID、訊息內容，因此只要該URI是可以接收POST的服務，
    # 就可以擷取user_id進行進一步動作

    def post(self):
        """ line bot response """
        payload = request.json
        print("------------")
        print(payload)  # for debug
        print("------------")
        response = None
        if webhook_message_checker(payload) == "text":
            invitation_url, replytoken = check_line_user(payload)
            print(f"reply token: {replytoken}")
            msg = {
                "type": "text",
                "text": f"感謝您使用小幫手，為了進一步確保服務品質，建議您點選以下連結註冊備援小幫手"
                f"連結: {invitation_url}"}

            sticker = {
                "type": "sticker",
                "packageId": "446",
                "stickerId": "1989"
            }

            json_for_msg = dict(
                replyToken=replytoken,
                messages=[msg, sticker]
            )
            print(f"json_for_msg: {json_for_msg}")
            result = urllib_requests.post(
                LineConstant.OFFICIAL_REPLY_API,
                headers=LineConstant.push_header,
                data=json_for_msg)
            print(f"reply status code: {result.status_code}")
            response = msg

        elif webhook_message_checker(payload) == "file":
            excel_handler()

        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK


@api.route("/who_serve")
class Serve(Resource):
    def get(self):
        """ connecting line notify to send free messeage """
        # TODO 改寫成輸入姓名，程式從JSON中尋找對應姓名的notify access token，藉此發送給特定人士
        response = {"hint": "服事者為Roykuo"}
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK
