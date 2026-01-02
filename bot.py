from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
from dotenv import load_dotenv


def start(update, context):
    update.message.reply_text("Здравствуйте")
    
def echo(update, context):
    update.message.reply_text(update.message.text)

def main():
    
    load_dotenv()
    TG_BOT_API=os.environ["TG_BOT_API"]

    logging.basicConfig(level=logging.INFO)

    updater = Updater(token=TG_BOT_API, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()
    

