
#!/bin/bash
set -e

echo "=== Починаємо відновлення системи Raspberry Pi Proxy ==="

echo "[1/8] Оновлення системи..."
sudo apt update -y && sudo apt upgrade -y

echo "[2/8] Встановлення необхідних пакетів..."
sudo apt install -y python3 python3-pip iptables-persistent git

echo "[3/8] Відновлення SSH ключів..."
mkdir -p ~/.ssh
cp ./backup/.ssh/* ~/.ssh/ 2>/dev/null || true
chmod 700 ~/.ssh
chmod 600 ~/.ssh/*

echo "[4/8] Відновлення Flask-сервера..."
cp -r ./backup/flask_server ~/flask_server
cd ~/flask_server
pip3 install -r requirements.txt

echo "[5/8] Відновлення конфігурації 3proxy..."
sudo mkdir -p /etc/3proxy
sudo cp -r ./backup/3proxy/* /etc/3proxy/
sudo systemctl enable 3proxy || true

echo "[6/8] Відновлення правил iptables..."
sudo iptables-restore < ./backup/iptables.rules
sudo netfilter-persistent save

echo "[7/8] Відновлення сервісів..."
sudo systemctl daemon-reload
sudo systemctl restart 3proxy || true

echo "[8/8] Встановлення автозапуску Flask-сервера..."
sudo cp ./backup/flask_server.service /etc/systemd/system/
sudo systemctl enable flask_server
sudo systemctl start flask_server

echo "=== Відновлення завершено! ==="
