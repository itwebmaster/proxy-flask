from flask import Blueprint, request, jsonify
from .auth import login_required
import os, subprocess

api_bp = Blueprint("api", __name__, url_prefix="/api")
API_KEY = os.environ.get("API_KEY")

def check_api_key(f):
    from functools import wraps
    from flask import request, jsonify
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.headers.get("X-API-KEY") != API_KEY:
            return jsonify({"error": "Invalid API Key"}), 403
        return f(*args, **kwargs)
    return decorated

@api_bp.route("/current_ip")
@login_required
@check_api_key
def current_ip():
    port = request.args.get("port")
    from .proxy import get_public_ip, PROXIES
    p = next((p for p in PROXIES if str(p["port"])==str(port)), None)
    if not p:
        return jsonify({"error":"Proxy not found"}), 404
    return jsonify({"port": port, "public_ip": get_public_ip(p["port"], p["user"], p["pass"])})

@api_bp.route("/run_script", methods=["POST"])
@login_required
@check_api_key
def run_script():
    data = request.json
    name = data.get("name")
    args = data.get("args", [])
    path = os.path.join("scripts", name)
    if not os.path.exists(path):
        return jsonify({"error": "Script not found"}), 404
    proc = subprocess.Popen([path]+args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return jsonify({"pid": proc.pid, "initial_output": []})

@api_bp.route("/restart_hilink", methods=["POST"])
@login_required
@check_api_key
def restart_hilink():
    # сюда вставить код переподключения HiLink
    return jsonify({"status":"ok"})
