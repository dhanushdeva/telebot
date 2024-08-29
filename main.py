from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = "7455381386:AAFgaSC0_ZlO-z4Q_TEoFoMDgZAjyB8Muvk"
BOT_USERNAME: Final = "@bbnnnabot"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me! I am Lotus!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am Lotus! Please type something so I can respond!')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command!')


 # this project initial basic to create a telegram reply message by me
 
def handle_response(text: str) -> str:
    processed: str = text.lower()
    if "hello" or "hi" in processed:
        return "Hey there!"
    if "how are you" in processed:
        return "I am good!"
    if "i need help" in processed:
        return "what the help you need from me!"
    if "i love python" in processed:
        return "Remember then you are going to achieve big!"
    if any(letter in processed for letter in ["abilash","benny","nitish","nitishkumar","muthu","muthukumar","muntazir","javith ahmed","gowtham"]):
        return "True friends and good people!"
    if any(name in processed for name in ["seiko","durai","duraimadhavan"]):
        return "try to focus on study!.Avoid using mobile!"
    if "abinesh" in processed:
        return "nignesh"
    if "i love you" in processed:
        return "Me too. Love you. But focus on study, don't get distracted!"
    if any(word in processed for word in ["fuck", "porn", "sex"]):
        return "You are a human being. Please check your words before reaching out to me!"

    return "I do not understand what you wrote!"

# Async function to handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type} : "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, ' ').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    print('Starting Bot...')
    app = Application.builder().token(TOKEN).build()

    # Command --> function call those functions()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)
    print('Polling')
    app.run_polling(poll_interval=3)
