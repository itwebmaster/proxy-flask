#!/bin/bash
echo "Restarting HiLink modem..."
# Приклад: перезапуск через curl
curl -s "http://192.168.8.1/api/device/control?operation=restart"
sleep 3
echo "Done."
