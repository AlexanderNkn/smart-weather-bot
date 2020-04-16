from telegram.ext import MessageHandler, Filters

from bot.handlers.handler import Handler
from bot.utils.weather import get_city_weather
from bot.texts import WEATHER_TEXT, UNKNOWN_ERROR_TEXT
from bot.keyboards import MAIN_MENU_KEYBOARD


class WeatherHandler(Handler):
    def __init__(self, dispatcher):
        self.handler = MessageHandler(Filters.regex(r"^.*(?i)show weather(?-i:)"), self.send_weather)

        super().__init__(dispatcher)

    def send_weather(self, update, context):
        city = context.user_data.get('city')
        if city is None:
            self.sender.message(update, 'Please, use command `/start/` to restart me.', MAIN_MENU_KEYBOARD)
            return
        weather = get_city_weather(city['id'], WEATHER_TEXT)
        if weather is None:
            self.sender.message(update, UNKNOWN_ERROR_TEXT, MAIN_MENU_KEYBOARD)
            return
        self.sender.message(update, weather, MAIN_MENU_KEYBOARD)
