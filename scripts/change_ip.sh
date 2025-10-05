#!/bin/bash
IFACE=$1

# Пример: сброс интерфейса и заново поднять
sudo ip link set $IFACE down
sleep 1
sudo ip link set $IFACE up

# Если нужен сброс модема через AT команды или API роутера, вставь сюда
# Например: sudo python3 /home/pi/scripts/reconnect_modem.py $IFACE
