# app.py
from flask import Flask, render_template, redirect, url_for
import subprocess
import requests
from functools import wraps

app = Flask(__name__)

# Настройки прокси: порт => логин/пароль
PROXIES = {
    4444: {"iface": "eth1", "user": "charter", "pass": "tickets2025"},
    4445: {"iface": "eth0", "user": "charter", "pass": "tickets2025"},
}

def get_public_ip(proxy_port, username, password):
    """Получаем публичный IP через прокси-порт"""
    proxy_url = f"http://{username}:{password}@127.0.0.1:{proxy_port}"
    proxies = {
        "http": proxy_url,
        "https": proxy_url
    }
    try:
        resp = requests.get("https://api.ipify.org", proxies=proxies, timeout=5)
        return resp.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/")
@login_required
def index():
    proxy_status = []
    for port, info in PROXIES.items():
        ip = get_public_ip(port, info["user"], info["pass"])
        proxy_status.append({
            "port": port,
            "iface": info["iface"],
            "public_ip": ip
        })
    return render_template("index.html", proxies=proxy_status)

@app.route("/restart/<int:port>")
def restart_proxy(port):
    # Вызов скрипта перезапуска прокси для конкретного порта
    # subprocess.call(["/home/ivan/scripts/restart_proxy.sh", str(port)])
    return redirect(url_for('index'))

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("auth_bp.login"))
        return f(*args, **kwargs)
    return decorated

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
