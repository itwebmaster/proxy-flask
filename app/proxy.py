import os
import requests

PROXIES = []

i = 1
while os.environ.get(f"PROXY_{i}_PORT"):
    PROXIES.append({
        "port": int(os.environ.get(f"PROXY_{i}_PORT")),
        "iface": os.environ.get(f"PROXY_{i}_IFACE"),
        "user": os.environ.get(f"PROXY_{i}_USER"),
        "pass": os.environ.get(f"PROXY_{i}_PASS"),
    })
    i += 1

def get_public_ip(proxy_port, username, password):
    proxy_url = f"http://{username}:{password}@127.0.0.1:{proxy_port}"
    proxies = {"http": proxy_url, "https": proxy_url}
    try:
        resp = requests.get("https://api.ipify.org", proxies=proxies, timeout=5)
        return resp.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"
