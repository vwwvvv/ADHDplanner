from fastapi import FastAPI, Request
from telegram import Bot, Update
import os
import json

app = FastAPI()

# Получаем токен из переменных окружения
TOKEN = os.getenv("BOT_TOKEN")

if TOKEN:
    bot = Bot(token=TOKEN)
else:
    bot = None
    print("WARNING: BOT_TOKEN not found")

@app.get("/")
async def root():
    """Корневой эндпоинт для проверки работы"""
    return {
        "message": "ADHD Planner Bot is running!", 
        "status": "ok",
        "token_available": bool(TOKEN),
        "bot_ready": bool(bot)
    }

@app.post("/")
async def webhook_handler(request: Request):
    """Обработчик webhook'ов от Telegram"""
    try:
        # Проверяем что бот инициализирован
        if not bot:
            return {"error": "Bot not initialized - check BOT_TOKEN", "ok": False}
        
        # Получаем данные от Telegram
        body = await request.body()
        data = json.loads(body)
        
        print(f"Received webhook data: {data}")
        
        # Создаем объект Update
        update = Update.de_json(data, bot)
        
        # Обрабатываем сообщение
        if update and update.message and update.message.text:
            await handle_message(update)
        
        return {"ok": True}
    
    except Exception as e:
        error_msg = f"Webhook error: {str(e)}"
        print(error_msg)
        return {"error": error_msg, "ok": False}

async def handle_message(update: Update):
    """Обработка входящих сообщений"""
    try:
        message = update.message
        chat_id = message.chat.id
        text = message.text
        
        print(f"Processing message: {text} from chat: {chat_id}")
        
        if text == "/start":
            welcome_text = (
                "🧠 Привет! Я ADHD Planner Bot!\n\n"
                "Я помогу тебе планировать задачи и не забывать важные дела.\n\n"
                "Доступные команды:\n"
                "/start - начать работу\n"
                "/help - помощь\n"
                "/plan - создать план"
            )
            await bot.send_message(chat_id=chat_id, text=welcome_text)
            
        elif text == "/help":
            help_text = (
                "📝 Помощь по ADHD Planner Bot:\n\n"
                "🎯 /plan - создать новый план\n"
                "⏰ Я помогу структурировать твой день!\n\n"
                "Просто отправь мне описание задачи."
            )
            await bot.send_message(chat_id=chat_id, text=help_text)
            
        elif text == "/plan":
            plan_text = (
                "📅 Создание плана:\n\n"
                "Отправь мне описание задачи, и я помогу её организовать!\n\n"
                "Например: 'Купить продукты завтра в 18:00'"
            )
            await bot.send_message(chat_id=chat_id, text=plan_text)
            
        else:
            # Обработка обычных сообщений
            response_text = (
                f"📝 Получил: '{text}'\n\n"
                "Используй /help для списка команд!"
            )
            await bot.send_message(chat_id=chat_id, text=response_text)
            
    except Exception as e:
        print(f"Error handling message: {e}")

# Для Vercel нужен именно этот handler
handler = app