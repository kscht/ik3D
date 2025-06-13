#!/bin/bash

# Проверка наличия python3
if ! command -v python3 &> /dev/null
then
    echo "python3 не найден. Пожалуйста, установите Python 3."
    exit 1
fi

# Создание виртуального окружения
python3 -m venv venv

# Активация виртуального окружения
source venv/bin/activate

# Обновление pip
pip install --upgrade pip

# Установка зависимостей
pip install -r requirements.txt

echo "Виртуальное окружение создано и зависимости установлены."

echo "Чтобы активировать виртуальное окружение, выполните:"
echo "source venv/bin/activate" 