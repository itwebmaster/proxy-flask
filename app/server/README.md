


cat > "$OUTDIR/README.txt" <<'EOF'
Export created on: '"$(date)"'
Contains: apt package list, systemd units, 3proxy configs, flask project (without venv), ssh public keys, iptables rules, network configs.
Before using bootstrap.sh: review files, DO NOT execute private keys blindly.
EOF

cat > "$OUTDIR/bootstrap.sh" <<'EOF'
#!/bin/bash
# BOOTSTRAP skeleton — edit before use: set USER, PROJECT_DIR, copy private keys manually
set -euo pipefail

USER=ivan
PROJECT_DIR=/home/$USER/projects/proxy-flask

# 1) update and essential packages
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git curl iproute2

# 2) create user (if not exists) and dirs
id -u "$USER" >/dev/null 2>&1 || sudo adduser --disabled-password --gecos "" "$USER"
sudo mkdir -p "$PROJECT_DIR"
sudo chown -R $USER:$USER $(dirname "$PROJECT_DIR")

# 3) restore apt sources (manually review before uncommenting)
# sudo cp ./apt_sources.list /etc/apt/sources.list
# sudo cp -r ./apt_sources_list.d/* /etc/apt/sources.list.d/

# 4) copy project files (assumes you placed archive contents in /tmp/setup)
# sudo cp -a /tmp/setup/projects/proxy-flask "$PROJECT_DIR"

# 5) create venv and install pip deps
sudo -u $USER /usr/bin/python3 -m venv "$PROJECT_DIR/venv"
sudo -u $USER "$PROJECT_DIR/venv/bin/pip" install --upgrade pip
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
  sudo -u $USER "$PROJECT_DIR/venv/bin/pip" install -r "$PROJECT_DIR/requirements.txt"
fi

# 6) restore 3proxy e
# sudo systemctl start 3proxy

# 7) restore systemd units
# sudo cp ./systemd_units/* /etc/systemd/system/Ф
# sudo systemctl daemon-reload
# sudo systemctl enable proxy-flask
# sudo systemctl start proxy-flask

echo "Bootstrap skeleton finished. Review manual steps and start services as needed."
EOF

chmod +x "$OUTDIR/bootstrap.sh"



cd "$HOME"
tar -czvf "${OUTDIR}.tar.gz" -C "$OUTDIR" .
echo "Export archive created: ${OUTDIR}.tar.gz"
