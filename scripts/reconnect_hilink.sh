#!/bin/bash
HILINK_IP="192.168.8.1"
LOG_FILE="${LOG_DIR:-/home/ivan/logs}/hilink.log"
IFACE="eth1"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

get_ip() {
  curl -s --max-time 5 https://api.ipify.org
}

log "🔁 Reconnect started ($IFACE)"
OLD_IP=$(get_ip)
log "🌐 Old IP: ${OLD_IP:-unknown}"

START=$(date +%s)

# 1️⃣ Отримуємо токен
TOKEN=$(curl -s http://$HILINK_IP/api/webserver/SesTokInfo)
COOKIE=$(echo "$TOKEN" | grep -oPm1 "(?<=<SesInfo>)[^<]+")
VERIF_TOKEN=$(echo "$TOKEN" | grep -oPm1 "(?<=<TokInfo>)[^<]+")

if [ -z "$VERIF_TOKEN" ]; then
  log "❌ Failed to get token"
  exit 1
fi

# 2️⃣ Вимикаємо з’єднання
curl -s -X POST \
  -H "Cookie: $COOKIE" \
  -H "__RequestVerificationToken: $VERIF_TOKEN" \
  -d "<request><dataswitch>0</dataswitch></request>" \
  http://$HILINK_IP/api/dialup/mobile-dataswitch > /dev/null

sleep 3

# 3️⃣ Отримуємо новий токен для підключення
TOKEN=$(curl -s http://$HILINK_IP/api/webserver/SesTokInfo)
COOKIE=$(echo "$TOKEN" | grep -oPm1 "(?<=<SesInfo>)[^<]+")
VERIF_TOKEN=$(echo "$TOKEN" | grep -oPm1 "(?<=<TokInfo>)[^<]+")

# 4️⃣ Увімкнення знову
curl -s -X POST \
  -H "Cookie: $COOKIE" \
  -H "__RequestVerificationToken: $VERIF_TOKEN" \
  -d "<request><dataswitch>1</dataswitch></request>" \
  http://$HILINK_IP/api/dialup/mobile-dataswitch > /dev/null

# 5️⃣ Чекаємо появи нового IP
sleep 6
NEW_IP=$(get_ip)
END=$(date +%s)
DURATION=$((END - START))

log "🌐 New IP: ${NEW_IP:-unknown}"
log "✅ Done in ${DURATION}s"
echo "Old IP: $OLD_IP"
echo "New IP: $NEW_IP"
echo "Done in ${DURATION}s"
