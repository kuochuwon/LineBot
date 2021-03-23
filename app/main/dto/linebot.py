from flask_restplus import Namespace, fields


class LineBotDto:
    api = Namespace(
        "linebot",
        description="Linebot related operations"
    )
    header = api.parser().add_argument("Authorization", location="headers", help="Bearer ")
    # get_all_device = api.model(
    #     "webhook",
    #     {
    #         "user": fields.String(required=True, description="User name"),
    #         "max_device": fields.Integer(
    #             required=False,
    #             description="numbers of device returned, ignore = default. 10, 0 = all"
    #         )
    #     }
    # )
