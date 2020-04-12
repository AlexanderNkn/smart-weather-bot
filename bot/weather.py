import requests
from datetime import datetime

from bot.config import OPEN_WEATHER_TOKEN


def get_city_weather(city_id):
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'id': city_id,
        'format': 'json',
        'appid': OPEN_WEATHER_TOKEN,
        'units': 'metric'
    }
    try:
        response = requests.get(url, params=params)
        return response.json()
    except requests.RequestException:
        return "Unknown error. Please try later."


def humanize_weather(weather, format):
    main = weather['main']
    wind = weather['wind']

    kwargs = {
        'city': weather['name'],
        'receiving': datetime.strftime(datetime.utcfromtimestamp(weather['dt']), '%H:%M'),
        'temperature': main['temp'],
        'pressure': main['pressure'],
        'humidity': main['humidity'],
        'wind_speed': wind['speed'],
        'wind_direction': wind['deg'],
        'additional_info': ''
    }

    return format.format(**kwargs)
