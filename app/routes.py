from flask import Blueprint, render_template, redirect, url_for
from .proxy import PROXIES, get_public_ip, restart_proxy_script

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
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

@main_bp.route("/restart/<int:port>")
def restart_proxy(port):
    restart_proxy_script(port)
    return redirect(url_for('main.index'))
