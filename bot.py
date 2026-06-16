import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import json
from datetime import datetime


FILE = "data.json"

def load():
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


homeworks = {
    "📐 Математика": "📐 Домашка:\n№5 стр 12\n\n📅 Дедлайн: завтра 18:00",
    "📖 Русский": "📖 Домашка:\nУпр 15\n\n📅 Дедлайн: пятница",
    "💻 Информатика": "💻 Домашка:\nСделать презентацию\n\n📅 Дедлайн: понедельник",
    "📅 Расписание": "📅 Расписание:\n1. Математика\n2. Русский\n3. Информатика",
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["📐 Математика"],
        ["📖 Русский"],
        ["💻 Информатика"],
        ["📅 Расписание"],
        ["⏰ Дедлайны"]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "📚 Система домашних заданий\n\nВыбери нужный раздел:",
        reply_markup=reply_markup
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "⏰ Дедлайны":
        data = load()
        deadlines = data["deadlines"]

        if not deadlines:
            await update.message.reply_text("Дедлайнов нет")
        else:
            msg = ""
            for d in deadlines:
                msg += f"📌 {d['subject']} — {d['task']} до {d['deadline']}\n"

            await update.message.reply_text(msg)

    elif text in homeworks:
        await update.message.reply_text(homeworks[text])


async def add_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        subject = context.args[0]
        task = context.args[1]
        deadline = context.args[2] + " " + context.args[3]

        data = load()

        data["deadlines"].append({
            "subject": subject,
            "task": task,
            "deadline": deadline
        })

        save(data)

        await update.message.reply_text("✅ Дедлайн добавлен")

    except:
        await update.message.reply_text(
            "❌ Формат:\n/add_deadline математика задача 2026-05-20 18:00"
        )

app = ApplicationBuilder().token("8622668650:AAGAE0JK6cAB_FWspv1J1DMJUmgD1qyScRw").build()

if __name__ == "__main__":
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_deadline", add_deadline))
    app.add_handler(MessageHandler(filters.TEXT, message))

    print("Бот запущен")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app.run_polling()