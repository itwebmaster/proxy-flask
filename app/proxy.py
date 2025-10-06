import subprocess
import requests

# Настройки прокси: порт => логин/пароль
PROXIES = {
    4444: {"iface": "eth1", "user": "charter", "pass": "tickets2025"},
    4445: {"iface": "eth0", "user": "charter", "pass": "tickets2025"},
}

def get_public_ip(proxy_port, username, password):
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

def restart_proxy_script(port):
    # Виклик bash скрипта для перезапуску конкретного порта
    subprocess.call(["/home/ivan/scripts/restart_proxy.sh", str(port)])
