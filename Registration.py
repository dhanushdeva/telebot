import logging
from imports import *
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, \
    ConversationHandler, ContextTypes
import requests
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

NAME, QUALIFICATION, COMMUNITY, GENDER = range(4)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    telegram_id = str(user.id)

    try:
        response = requests.get(f"{'http://127.0.0.1:8090/api/collections/exam'}?filter=(telegram_id='{telegram_id}')")
        response.raise_for_status()
        if response.json().get('items'):
            user_data = response.json()['items'][0]
            await update.message.reply_text(
                f"You are already registered with the following details:\n"
                f"Name: {user_data.get('name')}\n"
                f"Qualification: {user_data.get('qualification')}\n"
                f"Community: {user_data.get('community')}\n"
                f"Gender: {user_data.get('gender')}\n"
                "Send /edit to update your details."
            )
            return ConversationHandler.END
    except requests.RequestException as e:
        logger.error(f"Error checking user registration: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")
        return ConversationHandler.END

    await update.message.reply_text('Welcome! Please enter your name:')
    return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    name = update.message.text.strip()

    if not name or len(name) > 50:
        await update.message.reply_text("Please enter a valid name (1-50 characters).")
        return NAME

    context.user_data['name'] = name
    context.user_data['telegram_id'] = str(user.id)

    keyboard = [
        [InlineKeyboardButton("10th", callback_data='10th'),
         InlineKeyboardButton("12th", callback_data='12th'),
         InlineKeyboardButton("Any Degree", callback_data='Any Degree')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose your qualification:', reply_markup=reply_markup)
    return QUALIFICATION


async def qualification(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['qualification'] = query.data

    keyboard = [
        [InlineKeyboardButton("General", callback_data='General'),
         InlineKeyboardButton("OBC", callback_data='OBC')],
        [InlineKeyboardButton("EWS", callback_data='EWS'),
         InlineKeyboardButton("SC/ST", callback_data='SC/ST')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('Please choose your community:', reply_markup=reply_markup)
    return COMMUNITY


async def community(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['community'] = query.data

    keyboard = [
        [InlineKeyboardButton("Male", callback_data='Male'),
         InlineKeyboardButton("Female", callback_data='Female')],
        [InlineKeyboardButton("Prefer not to say", callback_data='Prefer not to say')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('Please choose your gender:', reply_markup=reply_markup)
    return GENDER


async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['gender'] = query.data

    data = {
        "name": context.user_data['name'],
        "qualification": context.user_data.get('qualification', ''),
        "community": context.user_data.get('community', ''),
        "gender": context.user_data.get('gender', ''),
        "telegram_id": context.user_data['telegram_id']
    }
    headers = {
        'Content-Type': 'application/json'
    }
    if POCKETBASE_API_TOKEN:
        headers['Authorization'] = f'Bearer {7123209873:AAG3ryFn1mByLO0S1v2B1DiU1thj9pqVj3A}'

    try:
        if 'record_id' in context.user_data:
            # Update existing record
            response = requests.patch(f"{'http://127.0.0.1:8090/api/collections/exam'}/{context.user_data['record_id']}", json=data, headers=headers)
        else:
            # Create new record
            response = requests.post(POCKETBASE_URL, json=data, headers=headers)
        response.raise_for_status()
        await query.edit_message_text('Registration successful!')
    except requests.RequestException as e:
        logger.error(f"Error saving user data: {e}")
        await query.edit_message_text('There was an error with your registration. Please try again.')

    return ConversationHandler.END


async def edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    telegram_id = str(user.id)

    try:
        response = requests.get(f"{'http://127.0.0.1:8090/api/collections/exam'}?filter=(telegram_id='{telegram_id}')")
        response.raise_for_status()
        if response.json().get('items'):
            user_data = response.json()['items'][0]
            context.user_data['record_id'] = user_data['id']
            await update.message.reply_text(
                f"Your current details:\n"
                f"Name: {user_data.get('name')}\n"
                f"Qualification: {user_data.get('qualification')}\n"
                f"Community: {user_data.get('community')}\n"
                f"Gender: {user_data.get('gender')}\n"
                "Please enter your name to update:"
            )
            return NAME
        else:
            await update.message.reply_text('You are not registered yet. Please use /start to register.')
            return ConversationHandler.END
    except requests.RequestException as e:
        logger.error(f"Error fetching user data: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")
        return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Registration process has been canceled.')
    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token('7123209873:AAG3ryFn1mByLO0S1v2B1DiU1thj9pqVj3A').build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('edit', edit)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            QUALIFICATION: [CallbackQueryHandler(qualification)],
            COMMUNITY: [CallbackQueryHandler(community)],
            GENDER: [CallbackQueryHandler(gender)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
