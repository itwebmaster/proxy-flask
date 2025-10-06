from flask import Flask, render_template, redirect, url_for, request, Response
from dotenv import load_dotenv
import subprocess
import requests
import os
from functools import wraps

load_dotenv()  # Загружаем .env

app = Flask(__name__)
app.config['DEBUG'] = os.getenv("DEBUG", "False").lower() == "true"

# --- HTTP Basic Auth ---
FLASK_PASSWORD = os.getenv("FLASK_PASSWORD", "supersecret")  # ставь свой пароль

def check_auth(password):
    return password == FLASK_PASSWORD

def authenticate():
    return Response(
        'Authentication required', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

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

# --- Маршруты ---
@app.route("/")
@requires_auth
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

