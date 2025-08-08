import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from datetime import datetime, timedelta

TASKS = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("➕ Добавить задачу", callback_data="add_task")],
        [InlineKeyboardButton("📅 Показать задачи", callback_data="show_tasks")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Я твой планер. Что хочешь сделать?", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "add_task":
        await query.edit_message_text("""Напиши задачу в свободном формате, например:

моноксер 15 мин
уборка 1.5 ч
домашка 90мин""")
    elif query.data == "show_tasks":
        if not TASKS:
            await query.edit_message_text("Пока задач нет.")
        else:
            text = "\n".join([f"{i+1}. {t['title']} — {t['duration']} мин" for i, t in enumerate(TASKS)])
            await query.edit_message_text(f"📅 Задачи на сегодня:\n\n{text}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    pattern = r"(\d+(?:[.,]\d+)?)\s*(ч|час|часа|часов|мин|м|минут|минуты|мин\.)"
    match = re.search(pattern, text)
    if match:
        duration_str, unit = match.groups()
        duration = float(duration_str.replace(',', '.'))
        if unit.startswith('ч'):
            duration_minutes = int(duration * 60)
        else:
            duration_minutes = int(duration)

        title = re.sub(pattern, '', text).strip()
        if not title:
            title = "Задача без названия"

        TASKS.append({"title": title, "duration": duration_minutes})
        await update.message.reply_text(f"✅ Задача «{title}» на {duration_minutes} мин добавлена!")
    else:
        await update.message.reply_text("❌ Не могу распознать время. Попробуй написать, например:\n\nмоноксер 15 мин\nуборка 1 час")

def main():
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
