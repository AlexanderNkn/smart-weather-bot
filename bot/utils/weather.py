import requests
from datetime import datetime
from datetime import timedelta

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


def humanize_weather(weather, pattern):
    main = weather['main']
    wind = weather['wind']
    print(weather)

    receiving = datetime.utcfromtimestamp(weather['dt']) + timedelta(seconds=weather['timezone'])

    additional_info = []

    weather_description = {}
    for description_element in weather['weather']:
        main_information = description_element['main']
        description = description_element['description']

        if main_information in weather_description:
            if len(description) > weather_description[main_information]:
                weather_description[main_information] = description
            continue
        weather_description[main_information] = description
    additional_info.append(", ".join(weather_description.values()).capitalize())

    if weather.get('clouds') is not None:
        additional_info.append(f"Clouds: {weather['clouds']['all']} %")

    rain = weather.get("rain")
    if rain is not None:
        rain_text = "Rain precipitation volume for {}: {}"
        if rain.get("1h") is not None:
            additional_info.append(rain_text.format("hour", rain['1h']))
        if rain.get("3h") is not None:
            additional_info.append(rain_text.format("3 hours", rain['3h']))

    snow = weather.get("snow")
    if snow is not None:
        snow_text = "Snow precipitation volume for {}: {}"
        if snow.get("1h") is not None:
            additional_info.append(snow_text.format("hour", snow['1h']))
        if snow.get("3h") is not None:
            additional_info.append(snow_text.format("3 hours", snow['3h']))

    kwargs = {
        'city': weather['name'],
        'receiving': datetime.strftime(receiving, '%H:%M'),
        'temperature': main['temp'],
        'pressure': main['pressure'],
        'humidity': main['humidity'],
        'wind_speed': wind['speed'],
        'wind_direction': wind['deg'],
        'additional_info': "\n".join(additional_info),
        'clothes': ''
    }

    return pattern.format(**kwargs)
