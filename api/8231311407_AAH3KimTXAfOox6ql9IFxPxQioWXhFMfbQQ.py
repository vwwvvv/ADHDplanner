from fastapi import FastAPI, Request
from telegram import Bot, Update
import os
import logging

app = FastAPI()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)

logging.basicConfig(level=logging.INFO)

@app.post("/")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        logging.info(f"Received update: {data}")

        update = Update.de_json(data, bot)

        if update.message and update.message.text == "/start":
            chat_id = update.message.chat.id
            await bot.send_message(chat_id=chat_id, text="Привет! Я на Vercel!")
            logging.info(f"Sent greeting to chat_id {chat_id}")

        return {"ok": True}
    except Exception as e:
        logging.error(f"Error handling update: {e}")
        return {"ok": False, "error": str(e)}
