from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Токен от BotFather
TOKEN = "7860332054:AAHhewKAqfQRML4eMoypQyOC62Kduz9BwiA"

# --- Обработчик команды /start ---
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

# --- Обработчик текстовых сообщений ---
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

# --- Основной запуск ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен! Ждёт сообщений...")
    app.run_polling()

# --- Точка входа ---
if __name__ == "__main__":
    main()
