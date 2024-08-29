from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

async def start(update: Update, context: CallbackContext):
    telegram_id = update.message.chat_id
    await update.message.reply_text(f"Your Telegram ID is {telegram_id}")

async def main():
    # Create the Application and pass it your bot's token.
    application = Application.builder().token('7123209873:AAG3ryFn1mByLO0S1v2B1DiU1thj9pqVj3A').build()

    # Add a handler for the /start command
    application.add_handler(CommandHandler('start', start))

    # Start the bot
    await application.start_polling()

    # Run the bot until you press Ctrl+C
    await application.idle()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
