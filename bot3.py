from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
from telegram.ext import AIORateLimiter, Application
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import filters
from aiohttp import web
import os
import logging

TOKEN =("7860332054:AAHhewKAqfQRML4eMoypQyOC62Kduz9BwiA")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # это твой Render URL, типа https://yourbot.onrender.com

logging.basicConfig(level=logging.INFO)

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📚 Помощь по предметам", "🧾 Шпаргалка"], ["📝 Задать вопрос", "📅 Расписание"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Я твой бот для помощи в учёбе.", reply_markup=markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    if user_text == "📚 помощь по предметам":
        await update.message.reply_text("Выбери предмет.")
    elif user_text == "🧾 шпаргалка":
        await update.message.reply_text("Напиши тему шпаргалки.")
    elif user_text == "📝 задать вопрос":
        await update.message.reply_text("Спроси что-нибудь.")
    elif user_text == "📅 расписание":
        await update.message.reply_text("Пока не настроено.")
    else:
        await update.message.reply_text("Я не понял. Выбери из меню.")

# Webhook setup
async def webhook(request):
    data = await request.json()
    await application.update_queue.put(Update.de_json(data, application.bot))
    return web.Response()

async def on_startup(app):
    await application.bot.set_webhook(f"{WEBHOOK_URL}/webhook")

application = Application.builder().token(TOKEN).rate_limiter(AIORateLimiter()).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Aiohttp app
web_app = web.Application()
web_app.add_routes([web.post('/webhook', webhook)])
web_app.on_startup.append(on_startup)

if __name__ == "__main__":
    web.run_app(web_app, port=int(os.environ.get("PORT", 10000)))
