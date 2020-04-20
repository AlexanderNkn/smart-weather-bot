import logging

from bot.bot import WeatherBot

logging.basicConfig(filename="bot.log", level=logging.DEBUG)

if __name__ == "__main__":
    bot = WeatherBot()
    bot.start_polling()
