import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("WEATHER_BOT_TOKEN")
OPEN_WEATHER_TOKEN = os.environ.get("OPEN_WEATHER_TOKEN")
TIMEZONEDB_TOKEN = os.environ.get("TIMEZONEDB_TOKEN") # https://timezonedb.com