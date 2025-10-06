from flask import Blueprint, render_template
from .auth import login_required
from .proxy import PROXIES, get_public_ip
import os

main_bp = Blueprint("main", __name__)
SCRIPTS_DIR = "scripts"

@main_bp.route("/")
@login_required
def index():
    proxy_status = []
    for p in PROXIES:
        ip = get_public_ip(p["port"], p["user"], p["pass"])
        proxy_status.append({**p, "public_ip": ip})

    from .logs import get_log_file_path
    log_path = get_log_file_path()

    scripts = [f for f in os.listdir(SCRIPTS_DIR) if os.path.isfile(os.path.join(SCRIPTS_DIR, f))]
    api_key = os.environ.get("API_KEY")

    return render_template("index.html",
                           proxies=proxy_status,
                           log_path=log_path,
                           scripts=scripts,
                           api_key=api_key)
