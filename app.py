from flask import Flask, render_template, jsonify, request
import subprocess
import socket

app = Flask(__name__)

# Интерфейсы и их прокси порты
PROXIES = {
    "eth0": 4444,
    "eth1": 4445
}

def get_interface_ip(interface):
    """Возвращает текущий IP интерфейса"""
    try:
        result = subprocess.check_output(
            ["ip", "addr", "show", interface], encoding="utf-8"
        )
        for line in result.split("\n"):
            line = line.strip()
            if line.startswith("inet "):
                return line.split()[1].split("/")[0]
    except subprocess.CalledProcessError:
        return None

def check_proxy(port, timeout=2):
    """Проверка доступности прокси через curl"""
    try:
        subprocess.check_output(
            ["curl", "-s", "--max-time", str(timeout), "-x", f"http://127.0.0.1:{port}", "http://ifconfig.me"],
            stderr=subprocess.DEVNULL,
            timeout=timeout+1
        )
        return True
    except subprocess.SubprocessError:
        return False

@app.route("/")
def index():
    status = {}
    for iface, port in PROXIES.items():
        ip = get_interface_ip(iface)
        proxy_ok = check_proxy(port)
        status[iface] = {
            "ip": ip,
            "port": port,
            "proxy_ok": proxy_ok
        }
    return render_template("index.html", status=status)

@app.route("/api/status")
def api_status():
    status = {}
    for iface, port in PROXIES.items():
        ip = get_interface_ip(iface)
        proxy_ok = check_proxy(port)
        status[iface] = {
            "ip": ip,
            "port": port,
            "proxy_ok": proxy_ok
        }
    return jsonify(status)

@app.route("/api/change_ip", methods=["POST"])
def change_ip():
    iface = request.json.get("interface")
    if iface not in PROXIES:
        return jsonify({"error": "Unknown interface"}), 400

    try:
        subprocess.run(["bash", "./scripts/change_ip.sh", iface], check=True)
        return jsonify({"status": "ok"})
    except subprocess.CalledProcessError:
        return jsonify({"status": "error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
