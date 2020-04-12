from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, RegexHandler

from bot.handlers.handler import Handler
from bot import cities
from bot.handlers.weather_handler import WeatherHandler


class LocationInputConversation(Handler):
    # States
    LOCATION_INPUT = 1
    LOCATION_CONFIRM = 2

    # Situations states
    TRY_AGAIN = 3

    TEXTS = {
        LOCATION_INPUT: "Please input your location.",
        LOCATION_CONFIRM: "{}\nIs it your location?",
        TRY_AGAIN: "I can't understand your location. Please, try again.",
        ConversationHandler.END: "Nice! Set your location - {}.\n" + WeatherHandler.MAIN_MENU_TEXT
    }

    KEYBOARDS = {
        LOCATION_INPUT: ReplyKeyboardMarkup(
            [[KeyboardButton(text="Send my location", request_location=True)]],
            resize_keyboard=True
        ),
        LOCATION_CONFIRM: ReplyKeyboardMarkup(
            [[KeyboardButton(text="Yes"), KeyboardButton(text="No")]],
            resize_keyboard=True
        ),
        ConversationHandler.END: WeatherHandler.MAIN_MENU_KEYBOARD
    }

    def __init__(self, dispatcher):
        self.handler = ConversationHandler(
            entry_points=[
                CommandHandler("start", self.handle_start),
                RegexHandler('Change my location', self.send_location_input)
            ],
            states={
                self.LOCATION_INPUT: [
                    MessageHandler(Filters.text, self.handle_location_input),
                    MessageHandler(Filters.location, self.handle_location_input)
                ],
                self.LOCATION_CONFIRM: [
                    MessageHandler(Filters.text, self.handle_location_confirm)
                ]
            },
            fallbacks=[],
            allow_reentry=True
        )
        super().__init__(dispatcher)

    def handle_start(self, update, context):
        if context.user_data.get('city') is not None:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=WeatherHandler.MAIN_MENU_TEXT,
                reply_markup=WeatherHandler.MAIN_MENU_KEYBOARD
            )
            return ConversationHandler.END

        return self.send_location_input(update, context)

    def send_location_input(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=self.TEXTS[self.LOCATION_INPUT],
            reply_markup=self.KEYBOARDS[self.LOCATION_INPUT]
        )
        return self.LOCATION_INPUT

    def handle_location_input(self, update, context):
        location = update.message.location
        if location is not None:
            found_cities = cities.find_city_by_coords(location.longitude, location.latitude)
        else:
            found_cities = cities.find_city(update.message.text)

        if len(found_cities) == 0:
            return self.send_try_again(update, context)

        if len(found_cities) == 1:
            city = found_cities[0]
            return self.handle_city_set(update, context, city)

        context.chat_data['found_cities'] = found_cities
        return self.send_location_confirmation(update, context)

    def send_location_confirmation(self, update, context):
        found_cities = context.chat_data['found_cities']
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=self.TEXTS[self.LOCATION_CONFIRM].format(found_cities[0]['name']),
            reply_markup=self.KEYBOARDS[self.LOCATION_CONFIRM]
        )
        return self.LOCATION_CONFIRM

    def send_try_again(self, update, context):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=self.TEXTS[self.TRY_AGAIN],
            reply_markup=self.KEYBOARDS[self.LOCATION_INPUT]
        )
        return self.LOCATION_INPUT

    def handle_location_confirm(self, update, context):
        if update.message.text == "Yes":
            return self.handle_city_set(update, context, context.chat_data["found_cities"][0])
        elif update.message.text == "No":
            found_cities = context.chat_data['found_cities']

            if len(found_cities) == 0:
                return self.send_try_again(update, context)

            context.chat_data['found_cities'].pop(0)
            return self.send_location_confirmation(update, context)

    def handle_city_set(self, update, context, city):
        context.user_data["city"] = city
        self.dispatcher.persistence.update_user_data(
            user_id=update.message.from_user.id,
            data=context.user_data
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=self.TEXTS[ConversationHandler.END].format(city['name']),
            reply_markup=self.KEYBOARDS[ConversationHandler.END]
        )
        return ConversationHandler.END
