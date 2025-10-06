from flask import Blueprint, Response
import time
import os
from datetime import datetime

LOG_DIR = "/var/log/3proxy"

logs_bp = Blueprint('logs', __name__, url_prefix='/logs')

def get_log_file_path():
    today_str = datetime.now().strftime("%d%m%y")  # формат 251006
    return os.path.join(LOG_DIR, f"3proxy-{today_str}.log")

def tail_f(file_path):
    """Генератор, який читає нові рядки з файлу (імітує tail -f)"""
    with open(file_path, "r") as f:
        f.seek(0, os.SEEK_END)  # йдемо в кінець файлу
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield f"data: {line}\n\n"

@logs_bp.route("/3proxy")
def stream_logs():
    file_path = get_log_file_path()
    if not os.path.exists(file_path):
        return "Log file not found", 404
    return Response(tail_f(file_path), mimetype='text/event-stream')
