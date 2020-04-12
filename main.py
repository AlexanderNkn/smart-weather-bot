from bot.bot import WeatherBot
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    bot = WeatherBot()
    bot.start()
