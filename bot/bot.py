from telegram.ext import Updater, PicklePersistence

from bot.config import BOT_TOKEN
from bot.handlers.location_input import LocationInputConversation
from bot.handlers.weather_handler import WeatherHandler


class WeatherBot:
    _HANDLERS = [
        LocationInputConversation,
        WeatherHandler
    ]

    def __init__(self):
        self.persistence = PicklePersistence(filename='bot.pickle')
        self.updater = Updater(token=BOT_TOKEN, use_context=True, persistence=self.persistence)

        self.dispatcher = self.updater.dispatcher
        self._init_handlers()

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def _init_handlers(self):
        for handler in self._HANDLERS:
            handler(self.dispatcher)
