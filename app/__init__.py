from flask_restplus import Api
from flask import Blueprint
from app.main import jwt
from app.main.controller.linebot_controller import api as line_ns


blueprint = Blueprint("api",
                      __name__,
                      url_prefix="/api/v1")
api = Api(blueprint,
          title="Roy Traffic light system demo",
          version="0.1.0",
          description="Roy Traffic light system demo")

jwt._set_error_handler_callbacks(api)

api.add_namespace(line_ns,
                  path="")
