MAIN_MENU_TEXT = "You can find out the current weather in your city or change your location."

LOCATION_INPUT_TEXT = "Please, input your city name."
LOCATION_CONFIRM_TEXT = "{}\nIs it your location?" # Country code and city name
TRY_AGAIN_TEXT = "I can't understand your location. Please, try again."
LOCATION_SET_TEXT = "Nice! Set your location - {}.\n" + MAIN_MENU_TEXT # City name

WEATHER_TEXT = """
☂️ Weather in 🌆 {city} at 🕙 {receiving}:
🌡️ Temperature: {temperature} °C
🌊 Humidity: {humidity} %
🌀 Atmospheric pressure: {pressure} hPa
💨 Wind speed: {wind_speed} meter/sec
💨 Wind direction: {wind_direction}°

{additional_info}

{clothes}
"""

RAIN_TEXT = "🌧️ Rain precipitation volume for {}: {}"
SNOW_TEXT = "❄️ Snow precipitation volume for {}: {}"
CLOUDS_TEXT = "☁️ Clouds: {} %"
WIND_GUST_TEXT = "💨 Wind gust: {}"