import requests
from datetime import datetime
from datetime import timedelta

from bot.config import OPEN_WEATHER_TOKEN
from bot.texts import (
    TEMPERATURE_TEXT,
    HUMIDITY_TEXT,
    PRESSURE_TEXT,
    WIND_SPEED_TEXT,
    WIND_DIRECTION_TEXT,
    RAIN_TEXT,
    SNOW_TEXT,
    CLOUDS_TEXT,
    WIND_GUST_TEXT,
    CLOTHES_RAIN_TEXT,
    CLOTHES_WIND_TEXT,
    CLOTHES_TEXT,
)


def get_city_weather(city_id, pattern):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "id": city_id,
        "format": "json",
        "appid": OPEN_WEATHER_TOKEN,
        "units": "metric",
    }
    try:
        response = requests.get(url, params=params)
        return humanize_weather(response.json(), pattern)
    except requests.RequestException:
        return


def humanize_weather(weather, pattern):
    main = weather["main"]

    receiving = datetime.utcfromtimestamp(weather["dt"]) + timedelta(seconds=weather["timezone"])

    weather_info = []

    if main.get('temp') is not None:
        weather_info.append(TEMPERATURE_TEXT.format(main['temp']))
    if main.get('pressure') is not None:
        weather_info.append(PRESSURE_TEXT.format(main['pressure']))
    if main.get('humidity') is not None:
        weather_info.append(HUMIDITY_TEXT.format(main['humidity']))

    wind = weather.get('wind')
    if wind:
        if wind.get('speed') is not None:
            weather_info.append(WIND_SPEED_TEXT.format(wind['speed']))
        if wind.get('deg') is not None:
            weather_info.append(WIND_DIRECTION_TEXT.format(wind['deg']))
        if wind.get('gust') is not None:
            weather_info.append(WIND_GUST_TEXT.format(wind['gust']))

    weather_description = {}
    for description_element in weather["weather"]:
        main_information = description_element["main"]
        description = description_element["description"]

        if main_information in weather_description:
            if len(description) > weather_description[main_information]:
                weather_description[main_information] = description
            continue
        weather_description[main_information] = description
    weather_info.append(", ".join(weather_description.values()).capitalize())

    if weather.get("clouds") is not None:
        weather_info.append(CLOUDS_TEXT.format(weather["clouds"]["all"]))

    rain = weather.get("rain")
    if rain is not None:
        if rain.get("1h") is not None:
            weather_info.append(RAIN_TEXT.format("hour", rain["1h"]))
        if rain.get("3h") is not None:
            weather_info.append(RAIN_TEXT.format("3 hours", rain["3h"]))

    snow = weather.get("snow")
    if snow is not None:
        if snow.get("1h") is not None:
            weather_info.append(SNOW_TEXT.format("hour", snow["1h"]))
        if snow.get("3h") is not None:
            weather_info.append(SNOW_TEXT.format("3 hours", snow["3h"]))

    kwargs = {
        "city": weather["name"],
        "receiving": datetime.strftime(receiving, "%H:%M"),
        "weather_info": "\n".join(weather_info),
        "clothes": get_clothes(weather),
    }

    return pattern.format(**kwargs)


def get_clothes(weather):
    main = weather["main"]
    temp = main.get('temp')
    if temp is None:
        return "Sorry, I can't recommend you anything because I don't know the temperature in your city."

    rain = weather.get("rain")

    heavy_wind = False
    wind = weather.get('wind')
    if wind is not None:
        if wind.get('speed') is not None:
            heavy_wind = weather["wind"]["speed"] > 6

    # First element of value is a clothes, second is a cause.
    # Clothes recommendations are extensible - we just need to add condition and value.
    temperature_dependency = {
        temp <= 0: ("something warm (a winter jacket, for example)", "cold"),
        0 < temp < 9: ("some autumn jacket or warm sweater", "a little cold"),
        9 <= temp <= 14: ("hoodie or sweater", "warm"),
        temp > 14 and not (rain or heavy_wind): ("T-shirt", "hot"),
        temp > 14 and rain: ("hoodie or raincoat", "rain"),
        temp > 14 and heavy_wind: ("windbreaker", "heavy wind"),
    }

    result = CLOTHES_TEXT.format(*temperature_dependency[True])
    if rain:
        result += CLOTHES_RAIN_TEXT
    if heavy_wind:
        result += CLOTHES_WIND_TEXT

    return result
