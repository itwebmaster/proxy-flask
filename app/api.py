# app/api.py
from flask import Blueprint, request, jsonify
import subprocess
import os
from datetime import datetime

api_bp = Blueprint("api_bp", __name__, url_prefix="/api")

LOG_DIR = os.environ.get("LOG_DIR", "./logs")
SCRIPTS_DIR = os.environ.get("SCRIPTS_DIR", "./scripts")

def log_action(message: str):
    """Додає запис у hilink.log з таймштампом"""
    os.makedirs(LOG_DIR, exist_ok=True)
    log_file = os.path.join(LOG_DIR, "hilink.log")
    with open(log_file, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

@api_bp.route("/reconnect_hilink", methods=["POST"])
def reconnect_hilink():
    """Перепідключає HiLink без повного перезапуску"""
    script_path = os.path.join(SCRIPTS_DIR, "reconnect_hilink.sh")

    if not os.path.exists(script_path):
        msg = f"❌ Script not found: {script_path}"
        log_action(msg)
        return jsonify({"status": "error", "message": msg}), 404

    try:
        result = subprocess.run(
            ["bash", script_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        msg = f"🔁 Reconnect executed: {script_path}\nSTDOUT: {result.stdout.strip()}\nSTDERR: {result.stderr.strip()}"
        log_action(msg)

        return jsonify({
            "status": "ok",
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        })

    except subprocess.TimeoutExpired:
        msg = f"⏰ Timeout during reconnect"
        log_action(msg)
        return jsonify({"status": "error", "message": msg}), 504


@api_bp.route("/restart_hilink", methods=["POST"])
def restart_hilink():
    """Перезапускає HiLink модем через скрипт"""
    script_path = os.path.join(SCRIPTS_DIR, "restart_hilink.sh")

    if not os.path.exists(script_path):
        msg = f"❌ Script not found: {script_path}"
        log_action(msg)
        return jsonify({"status": "error", "message": msg}), 404

    try:
        result = subprocess.run(
            ["bash", script_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        msg = f"✅ Restart executed: {script_path}\nSTDOUT: {result.stdout.strip()}\nSTDERR: {result.stderr.strip()}"
        log_action(msg)

        return jsonify({
            "status": "ok",
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        })

    except subprocess.TimeoutExpired:
        msg = f"⏰ Timeout: {script_path}"
        log_action(msg)
        return jsonify({"status": "error", "message": msg}), 504

    except Exception as e:
        msg = f"💥 Exception: {e}"
        log_action(msg)
        return jsonify({"status": "error", "message": str(e)}), 500
