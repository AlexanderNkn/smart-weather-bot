from flask import Flask, request, Response
import logging

from bot.bot import WeatherBot
from bot.config import BOT_TOKEN

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

bot = WeatherBot()
bot.register_webhook()


@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def process_update():
    bot.process_update(request.get_data().decode('utf-8'))
    return Response("ok", status=200)
