from fastapi import FastAPI, Request
from telegram import Bot, Update
import os

app = FastAPI()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)

@app.post("/")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)

    if update.message and update.message.text == "/start":
        chat_id = update.message.chat.id
        await bot.send_message(chat_id=chat_id, text="Привет! Я на Vercel!")
    return {"ok": True}
