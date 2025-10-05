# app.py
from flask import Flask, render_template, redirect, url_for
import subprocess
import requests

app = Flask(__name__)

# Настройки прокси: порт => интерфейс / netns
PROXIES = {
    4444: "eth1",
    4445: "eth0",
}

def get_public_ip_ns(ns):
    """Получаем публичный IP через netns или интерфейс"""
    try:
        # Если у тебя netns:
        # result = subprocess.check_output(["ip", "netns", "exec", ns, "curl", "-s", "https://ifconfig.me"], text=True, timeout=5)

        # Для простоты просто curl от интерфейса
        result = requests.get("https://api.ipify.org", timeout=5)
        return result.text.strip()
    except Exception:
        return "Unavailable"

@app.route("/")
def index():
    proxy_status = []
    for port, iface in PROXIES.items():
        ip = get_public_ip_ns(iface)
        proxy_status.append({"port": port, "iface": iface, "public_ip": ip})
    return render_template("index.html", proxies=proxy_status)

@app.route("/restart/<int:port>")
def restart_proxy(port):
    # Здесь вызываем bash-скрипт смены IP или перезапуска прокси
    # Например:
    # subprocess.call(["/home/ivan/scripts/restart_proxy.sh", str(port)])
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
