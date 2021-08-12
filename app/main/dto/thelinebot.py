from flask_restplus import Namespace, fields


class LineBotDto:
    dto_name = "linebot"
    ip_dto_name = "linebot ip service"
    api = Namespace(
        dto_name,
        description="Linebot related operations"
    )
    header = api.parser().add_argument("Authorization", location="headers", help="Bearer ")

    # HINT 先不用dto，因為Webhook會接收的訊息來源很多種
    # ip = api.model(
    #     ip_dto_name,
    #     {
    #         ""
    #     }

    # )
