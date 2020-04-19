import logging

from bot.bot import WeatherBot

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    bot = WeatherBot()
    bot.start_polling()
