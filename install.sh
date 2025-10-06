#!/bin/bash

# Название виртуального окружения
VENV_DIR="venv"

# Проверяем, есть ли venv
if [ ! -d "$VENV_DIR" ]; then
    echo "Создаю виртуальное окружение..."
    python3 -m venv $VENV_DIR
else
    echo "Виртуальное окружение уже существует."
fi

# Активируем venv
source $VENV_DIR/bin/activate

# Обновляем pip
pip install --upgrade pip

# Устанавливаем зависимости
if [ -f "requirements.txt" ]; then
    echo "Устанавливаю зависимости из requirements.txt..."
    pip install -r requirements.txt
else
    echo "Файл requirements.txt не найден!"
    exit 1
fi

# Создаем .env если его нет
if [ ! -f ".env" ]; then
    echo "Создаю файл .env..."
    cat <<EOL > .env
SECRET_KEY=supersecretkey
PASSWORD=mypassword
API_KEY=supersecretapikey
LOG_DIR=/var/log/3proxy
EOL
    echo ".env создан. Пожалуйста, проверьте и измените значения по необходимости."
else
    echo ".env уже существует."
fi

echo "Установка завершена. Чтобы активировать venv, выполните:"
echo "source $VENV_DIR/bin/activate"
