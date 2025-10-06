#!/bin/bash

HILINK_IP="192.168.8.1"
LOG_FILE="${LOG_DIR:-/home/ivan/logs}/hilink.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🔁 Restarting HiLink..." >> "$LOG_FILE"

TOKEN=$(curl -s http://$HILINK_IP/api/webserver/SesTokInfo)
COOKIE=$(echo "$TOKEN" | grep -oPm1 "(?<=<SesInfo>)[^<]+")
VERIF_TOKEN=$(echo "$TOKEN" | grep -oPm1 "(?<=<TokInfo>)[^<]+")

if [ -z "$VERIF_TOKEN" ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Failed to get token" >> "$LOG_FILE"
  exit 1
fi

RESP=$(curl -s -X POST \
  -H "Cookie: $COOKIE" \
  -H "__RequestVerificationToken: $VERIF_TOKEN" \
  -d "<request><Control>1</Control></request>" \
  http://$HILINK_IP/api/device/control)

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Response: $RESP" >> "$LOG_FILE"
echo "Done."
