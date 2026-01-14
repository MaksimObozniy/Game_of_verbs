import logging
import os
from telegram import Bot


class TelegramLogsHandler(logging.Handler):
    def __init__(self, token, chat_id):
        super().__init__()
        self.bot = Bot(token=token)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def setup_logging():
    bot_token=os.environ["TG_DEBUG_TOKEN"]
    chat_id=os.environ["TG_USER_ID"]
    
    logger = logging.getLogger("igra_glagolov")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    telegram_handler = TelegramLogsHandler(bot_token, chat_id)

    formatter = logging.Formatter(
        "%(asctime)s — %(levelname)s — %(message)s"
    )

    telegram_handler.setFormatter(formatter)

    logger.addHandler(telegram_handler)

    return logger
