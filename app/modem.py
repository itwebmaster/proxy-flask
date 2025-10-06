# app/modem.py
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

DEFAULT_MODEM_IP = "192.168.8.1"
TIMEOUT = 5

def _try_post(url, data, headers=None, auth=None):
    try:
        resp = requests.post(url, data=data, headers=headers or {}, auth=auth, timeout=TIMEOUT)
        return True, resp.text
    except Exception as e:
        return False, str(e)

def hilink_reconnect(modem_ip=DEFAULT_MODEM_IP, username=None, password=None):
    """
    Попытка выключить и включить мобильные данные через API
    возвращает (ok, response_text)
    """
    base = f"http://{modem_ip}"
    # наиболее часто используемый endpoint
    dataswitch_endpoint = f"{base}/api/dialup/mobile-dataswitch"
    payload_off = "<request><dataswitch>0</dataswitch></request>"
    payload_on  = "<request><dataswitch>1</dataswitch></request>"
    headers = {"Content-Type": "text/xml"}

    auth = None
    if username:
        auth = HTTPBasicAuth(username, password or "")

    ok, r1 = _try_post(dataswitch_endpoint, payload_off, headers=headers, auth=auth)
    # небольшая пауза
    import time; time.sleep(2)
    ok2, r2 = _try_post(dataswitch_endpoint, payload_on, headers=headers, auth=auth)
    return (ok and ok2), {"off": r1, "on": r2}

def hilink_reboot(modem_ip=DEFAULT_MODEM_IP, username=None, password=None):
    """
    Перезагрузка модема: пытаемся несколько известных endpoint'ов.
    """
    base = f"http://{modem_ip}"
    headers = {"Content-Type": "text/xml"}
    auth = None
    if username:
        from requests.auth import HTTPBasicAuth
        auth = HTTPBasicAuth(username, password or "")

    # endpoint, который иногда работает:
    reboot_endpoints = [
        f"{base}/api/device/control",   # может принимать XML с action=reboot
        f"{base}/api/device/reboot",
        f"{base}/api/maintenance/reboot",
    ]
    results = {}
    for ep in reboot_endpoints:
        payload = "<request><Control>reboot</Control></request>"
        ok, resp = _try_post(ep, payload, headers=headers, auth=auth)
        results[ep] = {"ok": ok, "resp": resp}
        if ok:
            return True, results
    return False, results
