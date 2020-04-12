from telegram.ext import Updater

from bot.config import BOT_TOKEN
from bot.handlers.echo_handler import EchoHandler


class WeatherBot:
    _HANDLERS = [
        EchoHandler
    ]

    def __init__(self):
        self.updater = Updater(token=BOT_TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self._init_handlers()

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def _init_handlers(self):
        for handler in self._HANDLERS:
            handler(self.dispatcher)
