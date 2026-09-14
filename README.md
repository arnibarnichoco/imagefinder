# Telegram Gemini Vision Bot

Минимальный Telegram-бот на Python. Он принимает фотографию, отправляет её в Gemini Vision и возвращает описание на русском языке. Подпись фотографии используется как запрос к модели. Если подписи нет, используется запрос `Опиши, что изображено на этой фотографии.`

## Установка

```bash
cd /opt/data/workspace/telegram_gemini_bot
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Настройка ключей

Скопируйте пример файла окружения:

```bash
cp .env.example .env
```

Откройте `.env` и заполните значения:

```dotenv
TELEGRAM_BOT_TOKEN=ваш_токен_бота_из_BotFather
GEMINI_API_KEY=ваш_ключ_Gemini
```

Файл `.env` содержит секреты и не должен коммититься. Он уже добавлен в `.gitignore`.

## Запуск

```bash
cd /opt/data/workspace/telegram_gemini_bot
source .venv/bin/activate
python agent.py
```

После запуска отправьте боту `/start`, `/help` или фотографию. Для фотографии можно добавить подпись с вопросом.

## Проверка без запуска бота

Проверка синтаксиса:

```bash
python -m py_compile agent.py
```

Polling в этом проекте запускается только при прямом выполнении `python agent.py`. Импорт модуля сам по себе не отправляет сообщения и не запускает polling.
