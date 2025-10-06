from flask import Blueprint, Response
from collections import deque
from datetime import datetime
import time, os

LOG_DIR = os.environ.get("LOG_DIR")
logs_bp = Blueprint("logs", __name__, url_prefix="/logs")

def get_log_file_path():
    today_str = datetime.now().strftime("%d%m%y")
    return os.path.join(LOG_DIR, f"3proxy-{today_str}.log")

def tail_f(file_path, last_n=50):
    lines = deque(maxlen=last_n)
    with open(file_path, "r") as f:
        for line in f:
            lines.append(line)
        yield f"data: {''.join(lines)}\n\n"
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            lines.append(line)
            yield f"data: {''.join(lines)}\n\n"

@logs_bp.route("/3proxy")
def stream_logs():
    file_path = get_log_file_path()
    if not os.path.exists(file_path):
        return "Log file not found", 404
    return Response(tail_f(file_path), mimetype="text/event-stream")
