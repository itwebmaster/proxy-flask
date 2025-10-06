
# Відновлення системи Raspberry Pi Proxy

## 1. Підготовка
- Встановіть чисту Raspberry Pi OS (Full).
- Підключіться по SSH або через монітор.
- Підключіть інтернет (Wi-Fi або Ethernet).

## 2. Розпакування архіву
```bash
cd ~
tar -xzvf rpi_proxy_backup.tar.gz
cd rpi_proxy_backup
```

## 3. Запуск скрипта відновлення
```bash
sudo chmod +x restore.sh
sudo ./restore.sh
```

## 4. Після відновлення
- Перевірте роботу Flask-сервера (http://localhost:5000 або ваш IP).
- Перевірте проксі на портах 4444 і 4445.
- Якщо потрібно, перезавантажте систему:
  ```bash
  sudo reboot
  ```
