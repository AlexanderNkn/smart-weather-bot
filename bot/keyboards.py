from telegram import ReplyKeyboardMarkup, KeyboardButton

MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup(
    [[KeyboardButton(text="☂️ Show weather")],
     [KeyboardButton(text="📍 Change my location")],
     [KeyboardButton(text="⏰ Daily weather notify")]],
    resize_keyboard=True
)

LOCATION_INPUT_KEYBOARD = ReplyKeyboardMarkup(
    [[KeyboardButton(text="📍 Send my location", request_location=True)]],
    resize_keyboard=True
)
LOCATION_CONFIRM_KEYBOARD = ReplyKeyboardMarkup(
    [[KeyboardButton(text="👍 Yes"), KeyboardButton(text="⛔ No")]],
    resize_keyboard=True
)

TIME_INPUT_KEYBOARD = ReplyKeyboardMarkup(
    [[KeyboardButton(text="06:00")], [KeyboardButton(text="08:00")], [KeyboardButton(text="10:00")]],
    resize_keyboard=True
)
