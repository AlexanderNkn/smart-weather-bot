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

_ONLY_TIME_KEYBOARD_BUTTONS = [
    [KeyboardButton(text="06:00")], [KeyboardButton(text="08:00")], [KeyboardButton(text="10:00")]
]

_DELETE_CURRENT_SUB_KEYBOARD_BUTTONS = _ONLY_TIME_KEYBOARD_BUTTONS + [
    [KeyboardButton(text="❌ Cancel my current subscription")]
]

ONLY_TIME_INPUT_KEYBOARD = ReplyKeyboardMarkup(
    _ONLY_TIME_KEYBOARD_BUTTONS,
    resize_keyboard=True
)

DELETE_CURRENT_SUB_KEYBOARD = ReplyKeyboardMarkup(
    _DELETE_CURRENT_SUB_KEYBOARD_BUTTONS,
    resize_keyboard=True
)
