"""Minimal Telegram bot that describes photos with Gemini Vision."""

import logging
import os
import tempfile
from pathlib import Path

import google.generativeai as genai
import telebot
from dotenv import load_dotenv


DEFAULT_PROMPT = "Опиши, что изображено на этой фотографии."
MODEL_NAME = "gemini-1.5-flash"

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_BOT_TOKEN or not GEMINI_API_KEY:
    raise RuntimeError(
        "Set TELEGRAM_BOT_TOKEN and GEMINI_API_KEY environment variables."
    )

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.reply_to(
        message,
        "Привет! Отправь фотографию, и я опишу, что на ней изображено.",
    )


@bot.message_handler(commands=["help"])
def handle_help(message):
    bot.reply_to(
        message,
        "Отправь фотографию. Можно добавить подпись с вопросом, "
        "или я просто опишу изображение.",
    )


@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    prompt = (message.caption or DEFAULT_PROMPT).strip() or DEFAULT_PROMPT
    temp_path = None

    try:
        bot.send_chat_action(message.chat.id, "typing")
        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        photo_bytes = bot.download_file(file_info.file_path)

        with tempfile.NamedTemporaryFile(suffix=Path(file_info.file_path).suffix or ".jpg", delete=False) as temp_file:
            temp_file.write(photo_bytes)
            temp_path = temp_file.name

        image = genai.upload_file(path=temp_path)
        response = model.generate_content([prompt, image])
        description = (response.text or "Не удалось получить описание изображения.").strip()
        bot.reply_to(message, description)
    except Exception:
        logger.exception("Failed to process photo")
        bot.reply_to(
            message,
            "Не удалось обработать фотографию. Попробуйте ещё раз позже.",
        )
    finally:
        if temp_path:
            try:
                os.remove(temp_path)
            except OSError:
                logger.warning("Could not remove temporary file", exc_info=True)


if __name__ == "__main__":
    bot.infinity_polling()
