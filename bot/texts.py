MAIN_MENU_TEXT = "Now you can find out the current weather in your city or change your location."

LOCATION_INPUT_TEXT = "Please, input your city name."
LOCATION_CONFIRM_TEXT = "{}\nIs it your location?" # Country code and city name
TRY_AGAIN_TEXT = "I can't understand your location. Please, try again."
LOCATION_SET_TEXT = "Nice! Set your location - {}.\n" + MAIN_MENU_TEXT # City name

TIME_INPUT_TEXT = "Ok, please input time you want to get weather information (use HH:MM format)"
TIME_SET_TEXT = "Nice! I will send you weather every day at {} in {} timezone.\n" \
                + MAIN_MENU_TEXT # time and timezone

CORONAVIRUS_WARNING = """😷 And if possible, don't leave home!
Self-isolation is the best way to win in this difficult situation in the world.
Be careful!
"""

WEATHER_TEXT = """
☂️ Weather in 🌆 {city} at 🕙 {receiving} (last up-to-date information):

{weather_info}

{clothes}

""" + CORONAVIRUS_WARNING

DAILY_WEATHER_TEXT = "Daily weather for you  😊\n" + WEATHER_TEXT

TEMPERATURE_TEXT = "🌡️ Temperature: {} °C"
HUMIDITY_TEXT = "🌊 Humidity: {} %"
PRESSURE_TEXT = "🌀 Atmospheric pressure: {} hPa"
WIND_SPEED_TEXT = "💨 Wind speed: {} meter/sec"
WIND_DIRECTION_TEXT = "💨 Wind direction: {}°"
WIND_GUST_TEXT = "💨 Wind gust: {}"
RAIN_TEXT = "🌧️ Rain precipitation volume for {}: {}"
SNOW_TEXT = "❄️ Snow precipitation volume for {}: {}"
CLOUDS_TEXT = "☁️ Clouds: {} %"
WEATHER_DESCRIPTION = "\n{}"

CLOTHES_TEXT = "👖 I recommend you to wear {} because it's {} now."
CLOTHES_WIND_TEXT = " Also you may need some kind of hat."
CLOTHES_RAIN_TEXT = " Don't forget to take an umbrella!"

UNKNOWN_ERROR_TEXT = "Unknown error. Please try later."