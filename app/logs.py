from flask import Blueprint, Response, stream_with_context
import os, time
from datetime import datetime

LOG_DIR = "/var/log/3proxy"

logs_bp = Blueprint('logs', __name__, url_prefix='/logs')

def get_log_file_path():
    today_str = datetime.now().strftime("%y%m%d")
    path = os.path.join(LOG_DIR, f"3proxy-{today_str}.log")
    # створюємо файл, якщо нема
    if not os.path.exists(path):
        open(path, 'a').close()
    return path

def tail_f(file_path):
    try:
        with open(file_path, "r") as f:
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if line:
                    yield f"data: {line}\n\n"
                else:
                    time.sleep(0.2)
    except Exception as e:
        yield f"data: Error: {str(e)}\n\n"

@logs_bp.route("/3proxy")
def stream_logs():
    file_path = get_log_file_path()
    return Response(stream_with_context(tail_f(file_path)), mimetype='text/event-stream')
