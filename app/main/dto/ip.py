from flask_restplus import Namespace, fields


class IpDto:
    api = Namespace(
        "ip",
        description="存取IP相關要求"
    )
    header = api.parser().add_argument("Authorization", location="headers", help="Bearer ")

    update_ip = api.model(
        "update_ip", {
            "win_ip": fields.String(example="127.0.0.1", description="Windows IP"),
            "wsl_ip": fields.String(example="172.0.0.1", description="WSL IP"),
            "port": fields.String(example="127.0.0.1", description="port"),
            "access_url": fields.String(example="127.0.0.1", description="用來存取目的地的URL")
        }
    )
