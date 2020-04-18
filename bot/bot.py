import json

from telegram import Update
from telegram.ext import Updater, PicklePersistence

from bot.config import BOT_TOKEN
from bot.handlers.daily_weather_handler import DailyWeatherHandler
from bot.handlers.location_input import LocationInputConversation
from bot.handlers.unknown_command_handler import UnknownCommandHandler
from bot.handlers.weather_handler import WeatherHandler


class WeatherBot:
    _HANDLERS = [
        LocationInputConversation,
        WeatherHandler,
        DailyWeatherHandler,
        UnknownCommandHandler
    ]

    def __init__(self):
        self.persistence = PicklePersistence(filename='bot.pickle', on_flush=True)
        self.updater = Updater(token=BOT_TOKEN, use_context=True, persistence=self.persistence)

        self.dispatcher = self.updater.dispatcher
        self._init_handlers()

    def register_webhook(self):
        self.updater.bot.delete_webhook()
        self.updater.bot.set_webhook(url=f'https://textgarbler.pythonanywhere.com/{BOT_TOKEN}')

    def process_update(self, raw_json):
        update = Update.de_json(json.loads(raw_json), self.updater.bot)
        self.dispatcher.process_update(update)

    def _init_handlers(self):
        for handler in self._HANDLERS:
            handler(self.dispatcher)
