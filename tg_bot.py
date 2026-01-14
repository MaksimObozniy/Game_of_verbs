import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
from dotenv import load_dotenv
from dialogflow_api import detect_intent_text
from logger import setup_logging


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Здравствуйте")


def handle_message(update: Update, context: CallbackContext) -> None:
    
    project_id = os.environ["PROJECT_ID"]
    
    user_text = update.message.text
    user_id = update.effective_user.id

    answer, is_fallback = detect_intent_text(
        project_id=project_id,
        session_id=str(user_id),
        text=user_text,
    )

    update.message.reply_text(answer)


def main():

    load_dotenv()
    tg_token = os.environ["TG_BOT_API"]

    logger = setup_logging()

    try:
        logger.info("Telegram бот был только что запущен!")
        updater = Updater(token=tg_token, use_context=True)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

        updater.start_polling()
        updater.idle()
        

    except Exception:
        logger.exception("Telegram бот упал с ошибкой!")
        raise


if __name__ == '__main__':
    main()
    

