from fastapi import FastAPI, Request, HTTPException
from telegram import Bot, Update
from telegram.error import TelegramError
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Получаем токен из переменных окружения
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    logger.error("BOT_TOKEN не найден в переменных окружения")
    raise ValueError("BOT_TOKEN не установлен")

bot = Bot(token=TOKEN)

@app.get("/")
async def root():
    """Корневой эндпоинт для проверки работы"""
    return {"message": "ADHD Planner Bot is running!", "status": "ok"}

@app.post("/")
async def webhook(request: Request):
    """Обработчик webhook'ов от Telegram"""
    try:
        # Получаем данные от Telegram
        data = await request.json()
        logger.info(f"Получен webhook: {data}")
        
        # Создаем объект Update
        update = Update.de_json(data, bot)
        
        # Обрабатываем сообщение
        if update.message:
            await handle_message(update)
        
        return {"ok": True}
    
    except Exception as e:
        logger.error(f"Ошибка обработки webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def handle_message(update: Update):
    """Обработка входящих сообщений"""
    message = update.message
    chat_id = message.chat.id
    text = message.text
    
    try:
        if text == "/start":
            welcome_text = (
                "🧠 Привет! Я ADHD Planner Bot!\n\n"
                "Я помогу тебе планировать задачи и не забывать важные дела.\n\n"
                "Доступные команды:\n"
                "/start - начать работу\n"
                "/help - помощь\n"
                "/plan - создать план\n"
                "/tasks - мои задачи"
            )
            await bot.send_message(chat_id=chat_id, text=welcome_text)
            
        elif text == "/help":
            help_text = (
                "📝 Помощь по ADHD Planner Bot:\n\n"
                "🎯 /plan - создать новый план или задачу\n"
                "📋 /tasks - посмотреть текущие задачи\n"
                "⏰ Я помогу тебе структурировать день и не забыть важное!\n\n"
                "Просто отправь мне описание задачи, и я помогу её организовать."
            )
            await bot.send_message(chat_id=chat_id, text=help_text)
            
        elif text == "/plan":
            plan_text = (
                "📅 Создание плана:\n\n"
                "Отправьте мне описание задачи в таком формате:\n"
                "• Что нужно сделать\n"
                "• Когда (время/дата)\n"
                "• Приоритет (высокий/средний/низкий)\n\n"
                "Пример: 'Купить продукты завтра в 18:00 высокий приоритет'"
            )
            await bot.send_message(chat_id=chat_id, text=plan_text)
            
        elif text == "/tasks":
            tasks_text = (
                "📋 Ваши задачи:\n\n"
                "Пока у вас нет сохраненных задач.\n"
                "Используйте /plan чтобы создать первую задачу!"
            )
            await bot.send_message(chat_id=chat_id, text=tasks_text)
            
        else:
            # Обработка обычных сообщений как потенциальных задач
            if len(text) > 5:  # Если сообщение содержательное
                response_text = (
                    f"📝 Получил задачу: '{text}'\n\n"
                    "Хочешь превратить это в план?\n"
                    "Используй /plan для структурированного планирования!"
                )
            else:
                response_text = (
                    "🤔 Не понял команду.\n"
                    "Используй /help для списка доступных команд."
                )
            
            await bot.send_message(chat_id=chat_id, text=response_text)
            
    except TelegramError as e:
        logger.error(f"Ошибка Telegram API: {e}")
    except Exception as e:
        logger.error(f"Общая ошибка при обработке сообщения: {e}")

# Для локального запуска
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)