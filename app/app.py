from flask import Flask, render_template, redirect, url_for, request
from dotenv import load_dotenv
import subprocess
import requests
import os

load_dotenv()  # Загружаем .env

app = Flask(__name__)
app.config['DEBUG'] = os.getenv("DEBUG", "False").lower() == "true"

# --- Загружаем прокси из .env ---
def load_proxies():
    proxies = {}
    i = 1
    while True:
        port = os.getenv(f"PROXY_{i}_PORT")
        if not port:
            break
        proxies[int(port)] = {
            "iface": os.getenv(f"PROXY_{i}_IFACE"),
            "user": os.getenv(f"PROXY_{i}_USER"),
            "pass": os.getenv(f"PROXY_{i}_PASS"),
        }
        i += 1
    return proxies

PROXIES = load_proxies()

def get_public_ip(proxy_port, username, password):
    """Получаем публичный IP через прокси"""
    proxy_url = f"http://{username}:{password}@127.0.0.1:{proxy_port}"
    proxies = {"http": proxy_url, "https": proxy_url}
    try:
        resp = requests.get("https://api.ipify.org", proxies=proxies, timeout=5)
        return resp.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/")
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
    # перезапускаем конкретный прокси (пример — вызываем shell-скрипт)
    script_path = f"/home/ivan/scripts/restart_proxy.sh"
    subprocess.call([script_path, str(port)])
    return redirect(url_for('index'))

@app.route("/api/restart_hilink", methods=["POST"])
def restart_hilink():
    api_key = request.headers.get("X-API-KEY")
    if api_key != os.getenv("API_KEY"):
        return {"error": "Unauthorized"}, 403

    script_path = "/home/ivan/scripts/restart_hilink.sh"
    if os.path.exists(script_path):
        subprocess.call([script_path])
        return {"status": "restarted"}
    return {"error": "Script not found"}, 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
