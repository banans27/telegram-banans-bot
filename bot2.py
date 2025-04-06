from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN", "7860332054:AAHhewKAqfQRML4eMoypQyOC62Kduz9BwiA")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📚 Помощь по предметам", "🧾 Шпаргалка"],
        ["📝 Задать вопрос", "📅 Расписание"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Привет! Я твой бот для помощи в учёбе. Чем помочь?",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()

    if user_text == "📚 помощь по предметам":
        await update.message.reply_text("Выбери предмет: математика, физика, история и т.д.")
    elif user_text == "🧾 шпаргалка":
        await update.message.reply_text("Напиши тему, по которой нужна шпаргалка. Пример: 'Шпаргалка по биологии: клетки'")
    elif user_text == "📝 задать вопрос":
        await update.message.reply_text("Спроси что угодно по школьной программе — постараюсь помочь!")
    elif user_text == "📅 расписание":
        await update.message.reply_text("Расписание пока не настроено. Хочешь, добавим функционал с напоминаниями о домашке?")
    else:
        await update.message.reply_text("Я не совсем понял. Выбери действие из меню или напиши вопрос.")

def main():
    # Создаем экземпляр бота с обработкой ошибок
    application = ApplicationBuilder().token(TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Настройка для работы на Render
    if os.getenv('RENDER'):
        logger.info("Запуск бота в режиме Render Background Worker")
        # Устанавливаем параметры polling для стабильной работы
        application.run_polling(
            poll_interval=3.0,
            timeout=20,
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )
    else:
        logger.info("Запуск бота в локальном режиме")
        application.run_polling()

if __name__ == "__main__":
    main()