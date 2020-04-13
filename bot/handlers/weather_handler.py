from telegram.ext import MessageHandler, Filters

from bot.handlers.handler import Handler
from bot.weather import get_city_weather, humanize_weather
from bot.texts import WEATHER_TEXT
from bot.keyboards import MAIN_MENU_KEYBOARD


class WeatherHandler(Handler):
    def __init__(self, dispatcher):
        self.handler = MessageHandler(Filters.regex("(?i)show weather(?-i:)"), self.send_weather)

        super().__init__(dispatcher)

    def send_weather(self, update, context):
        city_id = context.user_data['city']['id']
        weather = get_city_weather(city_id)
        self.sender.message(update, humanize_weather(weather, WEATHER_TEXT), MAIN_MENU_KEYBOARD)
