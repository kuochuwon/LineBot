from flask import request
from flask_api import status
from flask_restplus import Resource
from app.main.dto.ip import IpDto
from app.main.service import ret
from app.main.service.ip_service import update_current_ip

api = IpDto.api
_header = IpDto.header
_update_ip = IpDto.update_ip

response_status = {status.HTTP_200_OK: ret.get_code_full(ret.RET_OK),
                   status.HTTP_401_UNAUTHORIZED: ret.get_code_full(ret.RET_NO_CUST_ID),
                   status.HTTP_404_NOT_FOUND: ret.get_code_full(ret.RET_NOT_FOUND)}


@api.route("/update_ip")
class UpdateIP(Resource):
    @api.expect(_header, _update_ip, validate=True)
    @api.doc(responses=response_status)
    def post(self):
        """更新雲端上的IP紀錄"""
        # TODO Need exception handling
        data = request.json
        win_ip = data.get("win_ip")
        wsl_ip = data.get("wsl_ip")
        update_current_ip(win_ip, wsl_ip)
        response = {"update_ip": f"{win_ip} / {wsl_ip}"}
        return ret.http_resp(ret.RET_OK, extra=response), status.HTTP_200_OK
