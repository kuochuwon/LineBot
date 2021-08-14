import os
from pathlib import Path


def get_current_ip():
    print(Path.cwd())
    with open(Path("ip_memo.txt"), "r", encoding="utf-8") as f:
        lines = f.readline()
        all_ip = lines.split(" ")
        win_ip = all_ip[0]
        wsl_ip = all_ip[1]
    return win_ip, wsl_ip


def get_access_url(ip, port):
    flask_url = f"http://{ip}:{port}/api/v1"
    return flask_url
