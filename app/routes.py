from flask import Blueprint, render_template, jsonify
import requests
from threading import Thread
import time
import os
from datetime import datetime

main_bp = Blueprint('main', __name__)

# Проксі
PROXIES = {
    4444: {"iface": "eth1", "user": "charter", "pass": "tickets2025", "public_ip": "0.0.0.0"},
    4445: {"iface": "eth0", "user": "charter", "pass": "tickets2025", "public_ip": "0.0.0.0"},
}



def get_log_file_path():
    today_str = datetime.now().strftime("%y%m%d")
    path = os.path.join("/var/log/3proxy", f"3proxy-{today_str}.log")
    # створюємо файл, якщо його нема
    if not os.path.exists(path):
        open(path, 'a').close()
    return path


def get_public_ip(proxy_port, username, password):
    proxy_url = f"http://{username}:{password}@127.0.0.1:{proxy_port}"
    proxies = {"http": proxy_url, "https": proxy_url}
    try:
        resp = requests.get("https://api.ipify.org", proxies=proxies, timeout=5)
        return resp.text.strip()
    except:
        return "Error"

def update_ips():
    while True:
        for port, info in PROXIES.items():
            info["public_ip"] = get_public_ip(port, info["user"], info["pass"])
        time.sleep(60)  # оновлення кожну хвилину

# Старт оновлення IP у фоновому потоці
thread = Thread(target=update_ips, daemon=True)
thread.start()

@main_bp.route('/')
def index():
    return render_template("index.html", proxies=PROXIES)

# API для автопідвантаження IP через JS
@main_bp.route('/api/proxies')
def api_proxies():
    return jsonify(PROXIES)

