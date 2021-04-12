from app.main.dto.thelinebot import LineBotDto
from app.main.service import ret
from app.main.constant import LineConstant
from app.main.util.common import (aaa_verify, api_exception_handler,
                                  check_access_authority)
from flask import request
import requests as urllib_requests
from flask_api import status
from flask_restplus import Resource
# from linebot import LineBotApi, WebhookHandler
# from linebot.models import MessageEvent, TextMessage, TextSendMessage, messages
# from werkzeug.exceptions import NotFound

api = LineBotDto.api
response_status = {status.HTTP_200_OK: ret.get_code_full(ret.RET_OK),
                   status.HTTP_401_UNAUTHORIZED: ret.get_code_full(ret.RET_NO_CUST_ID),
                   status.HTTP_404_NOT_FOUND: ret.get_code_full(ret.RET_NOT_FOUND)}


@api.route("/notify")
class LineNotify(Resource):
    def post(self):
        """ connecting line notify to send free messeage """
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
                params=json_for_msg)
            if result.status_code == 200:
                response = {"hint": "訊息發送成功"}

        # if payload.get("events"):
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK


@api.route("/push")
class Push(Resource):
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
    # 學你說話
    # @handler.add(MessageEvent, message=TextMessage)
    # def echo(event):
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text=event.message.text)
    #     )

    # @api.expect(_header, _get_all_device,
    #             validate=True)
    # @api.doc(responses=response_status)
    # @jwt_required
    # @check_access_authority
    @api_exception_handler
    def post(self):
        """ line bot response """

        # to = "YOUR USER ID"

        # line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        payload = request.json
        print("------------")
        print(payload)  # for debug
        print("------------")
        response = None
        if payload.get("events"):
            temp = payload.get("events")[0]
            timestamp = temp.get("timestamp")
            msg_dict: dict = temp.get("message")
            msg_type = msg_dict.get("type")
            msg_text = msg_dict.get("text")
            response = dict(
                timestamp=timestamp,
                msg_type=msg_type,
                msg_text=msg_text
            )

        # if not response:
        #     raise NotFound(ret.http_resp(ret.RET_NOT_FOUND))
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK
