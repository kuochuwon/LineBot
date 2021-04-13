import json
from app.main.dto.thelinebot import LineBotDto
from app.main.service import ret
from app.main.constant import LineConstant
from app.main.util.common import (aaa_verify, api_exception_handler,
                                  check_access_authority)
from app.main.view.linebot_response import check_line_user
from flask import request
import requests as urllib_requests
from flask_api import status
from flask_restplus import Resource
from lotify.client import Client
# from linebot import LineBotApi, WebhookHandler
# from linebot.models import MessageEvent, TextMessage, TextSendMessage, messages
# from werkzeug.exceptions import NotFound

api = LineBotDto.api
response_status = {status.HTTP_200_OK: ret.get_code_full(ret.RET_OK),
                   status.HTTP_401_UNAUTHORIZED: ret.get_code_full(ret.RET_NO_CUST_ID),
                   status.HTTP_404_NOT_FOUND: ret.get_code_full(ret.RET_NOT_FOUND)}


@api.route("/callback")
class Callback(Resource):
    def post(self):
        """ line bot response """
        # payload = request.json
        code = request.form.get('code')
        state = request.form.get('state')
        files = {
            "grant_type": "authorization_code",
            "redirect_uri": "http://127.0.0.1:5000/api/v1/linebot/callback",
            "client_id": "UulwSUMmf5M9zY1HSTR8xy",
            "client_secret": "MDuIohlUsEsPRKP2VXq0weJAW3cYwbb24gfeixTDmVC",
            "code": code
        }
        print("------------")
        print(code)  # for debug
        print("------------")
        session = urllib_requests.Session()
        result = session.post(
            LineConstant.OFFICIAL_OAUTH_API,
            headers={'User-Agent': 'Mozilla/5.0'},
            params=files
        )
        # result = urllib_requests.post(
        #     LineConstant.OFFICIAL_OAUTH_API,
        #     files=files)
        # temp = LineConstant.NOTIFY.get("CLIENT_ID")
        # lotify = Client(client_id=LineConstant.NOTIFY.get("CLIENT_ID"),
        #                 client_secret=LineConstant.NOTIFY.get("SECRET"),
        #                 redirect_uri=LineConstant.NOTIFY.get("URI"))
        # print(lotify)
        # token = lotify.get_access_token(code=request.args.get("svNW0IDGpqQPGDsBVFpJ20"))
        # print(token)
        output = result.text
        response = None
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK


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
    # HINT 技術原理與流程: 使用者向linebot發送訊息，
    # line server收到後會向指定的URI發出一個POST請求，
    # 並包含使用者ID、訊息內容，因此只要該URI是可以接收POST的服務，
    # 就可以擷取user_id進行進一步動作

    # @api.expect(_header, _get_all_device,
    #             validate=True)
    # @api.doc(responses=response_status)
    # @jwt_required
    # @check_access_authority
    # @api_exception_handler
    def post(self):
        """ line bot response """
        payload = request.json
        print("------------")
        print(payload)  # for debug
        print("------------")
        response = None
        if payload.get("events"):
            invitation_url = check_line_user(payload)
            response = {"hint": f"感謝您使用小幫手，為了進一步確保服務品質，建議您點選以下連結註冊備援小幫手"
                        f"連結: {invitation_url}"}
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK
