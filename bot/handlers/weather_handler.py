from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import MessageHandler, Filters

from bot.handlers.handler import Handler
from bot.weather import get_city_weather, humanize_weather


class WeatherHandler(Handler):
    MAIN_MENU_TEXT = "You can find out the current weather in your city or change your location."
    MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup(
        [[KeyboardButton(text="Show weather")], [KeyboardButton(text="Change my location")]],
        resize_keyboard=True
    )

    WEATHER_TEXT = """
Weather in {city} at {receiving}:
Temperature: {temperature} °C
Humidity: {humidity} %
Atmospheric pressure: {pressure} hPa
Wind speed: {wind_speed} meter/sec
Wind direction: {wind_direction}°
{additional_info}
"""

    def __init__(self, dispatcher):
        self.handler = MessageHandler(Filters.text, self.send_weather)

        super().__init__(dispatcher)

    def send_weather(self, update, context):
        city_id = context.user_data['city']['id']
        weather = get_city_weather(city_id)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=humanize_weather(weather, self.WEATHER_TEXT),
            reply_markup=self.MAIN_MENU_KEYBOARD
        )
