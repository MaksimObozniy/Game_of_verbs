import logging
import os
from telegram import Bot


logs_bot = None
tg_chat_id = None


class TelegramLogsHandler(logging.Handler):
    def emit(self, record):
        log_message = self.format(record)

        if logs_bot and tg_chat_id:
            logs_bot.send_message(chat_id=tg_chat_id, text=log_message)


def setup_logging():
    global logs_bot, tg_chat_id

    tg_chat_id = os.environ["TG_USER_ID"]
    token = os.environ["TG_DEBUG_TOKEN"]

    if not tg_chat_id or not token:
        return

    logs_bot = Bot(token=token)

    telegram_handler = TelegramLogsHandler()
    telegram_handler.setLevel(logging.ERROR)

    formater = logging.Formater(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    telegram_handler.setFormatter(formater)

    logging.getLogger().addHandler(telegram_handler)