import requests as urllib_requests
from app.main.constant import LineConstant
from app.main.log import logger
from app.main.dto.thelinebot import LineBotDto
from app.main.service import ret
from app.main.view.linebot_response import (
    church_file_handler, notify_handler, retrieve_notify_token_from_callback,
    church_text_handler, webhook_message_checker)
from flask import request
from flask_api import status
from flask_restplus import Resource

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
        payload = request.json
        # print("------------")
        # print(payload)  # for debug
        logger.debug(f"notify payload: {payload}")
        # print("------------")

        response = notify_handler(payload)

        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK


@api.route("/push")
class Push(Resource):
    def post(self):
        """ connecting line bot API to push messeage """
        payload = request.json

        logger.debug(f"push payload: {payload}")
        response = {"hint": "已接收請求，但內容為空"}
        try:
            user_id = payload.get("user_id")
            text = payload.get("text")
            token_identifier = payload.get("token_identifier")
            json_for_msg = dict(
                to=user_id,
                messages=[{
                    "type": "text",
                    "text": text
                }]
            )
            result = urllib_requests.post(
                LineConstant.OFFICIAL_PUSH_API,
                headers=LineConstant().generate_push_or_reply_header(token_identifier),
                json=json_for_msg)
            if result.status_code == 200:
                response = {"hint": "訊息發送成功"}
                return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK
        except Exception as e:
            # print(f"push failed: {e}")
            logger.exception(f"push failed: {e}")
            return ret.http_resp(ret.RET_EXCEPTION, extra={"hint": str(e)}), status.HTTP_503_SERVICE_UNAVAILABLE


@api.route("/7pct_webhook")
class Church_Webhook(Resource):
    # HINT 技術原理與流程: 使用者向linebot發送訊息，
    # line server收到後會向指定的URI發出一個POST請求，
    # 並包含使用者ID、訊息內容，因此只要該URI是可以接收POST的服務，
    # 就可以擷取user_id進行進一步動作

    def post(self):
        """ line bot response """
        payload = request.json
        logger.debug(f"webhook payload: {payload}")
        identifier = "7PCT_helper"
        response = None
        if webhook_message_checker(payload) == "text":
            response = church_text_handler(payload, identifier)
        elif webhook_message_checker(payload) == "file":
            response = church_file_handler(payload, identifier)

        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK


@api.route("/IP_webhook")
class IP_Webhook(Resource):
    def post(self):
        """ line bot response """
        payload = request.json
        logger.debug(f"webhook payload: {payload}")
        identifier = "IP_service"
        response = None
        if webhook_message_checker(payload) == "text":
            response = church_text_handler(payload)

        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK
