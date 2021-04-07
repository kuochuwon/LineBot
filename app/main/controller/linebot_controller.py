from app.main.dto.thelinebot import LineBotDto
from app.main.service import ret
from app.main.util.common import (aaa_verify, api_exception_handler,
                                  check_access_authority)
from flask import request
from flask_api import status
from flask_restplus import Resource
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from werkzeug.exceptions import NotFound

api = LineBotDto.api
response_status = {status.HTTP_200_OK: ret.get_code_full(ret.RET_OK),
                   status.HTTP_401_UNAUTHORIZED: ret.get_code_full(ret.RET_NO_CUST_ID),
                   status.HTTP_404_NOT_FOUND: ret.get_code_full(ret.RET_NOT_FOUND)}

CHANNEL_ACCESS_TOKEN = """
qipp53w9dsKIjaDG3D5eYswChigJUmYdgD6ilha3BCHjF4rJmG8dVjj3kMqpBy4TvTnYODobZelFc5bsSz9ycEx09y
/XU3aZO42Bp2o0+9f9TRJBFMeUih6Oi2YB77ET4+u5z/miOF5FRihh5ubRTgdB04t89/1O/w1cDnyilFU=
"""

CHANNEL_SECRET_TOKEN = """
6fd6a21c86d311aaf115d9588cc5fc46
"""

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET_TOKEN)


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
        payload: dict = request.json
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

        if not response:
            raise NotFound(ret.http_resp(ret.RET_NOT_FOUND))
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK
