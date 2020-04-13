from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    Filters,
)

from bot.handlers.handler import Handler
from bot.utils import cities
from bot.texts import (
    MAIN_MENU_TEXT,
    LOCATION_INPUT_TEXT,
    LOCATION_CONFIRM_TEXT,
    LOCATION_SET_TEXT,
    TRY_AGAIN_TEXT,
)
from bot.keyboards import (
    MAIN_MENU_KEYBOARD,
    LOCATION_INPUT_KEYBOARD,
    LOCATION_CONFIRM_KEYBOARD,
)


class LocationInputConversation(Handler):
    # States
    LOCATION_INPUT = 1
    LOCATION_CONFIRM = 2

    # States without own handling
    TRY_AGAIN = 3

    def __init__(self, dispatcher):
        self.handler = ConversationHandler(
            entry_points=[
                CommandHandler("start", self.handle_start),
                MessageHandler(Filters.regex(r"^.*(?i)change my location(?-i:)"), self.send_location_input),
            ],
            states={
                self.LOCATION_INPUT: [
                    MessageHandler(Filters.text, self.handle_location_input),
                    MessageHandler(Filters.location, self.handle_location_input),
                ],
                self.LOCATION_CONFIRM: [
                    MessageHandler(Filters.regex(r"^.*(?i)yes|no(?-i:)"), self.handle_location_confirm)
                ],
            },
            fallbacks=[],
            allow_reentry=True,
        )
        super().__init__(dispatcher)

    def handle_start(self, update, context):
        if context.user_data.get("city") is not None:
            # User does not need to input location with /start if he already has one
            self.sender.message(update, MAIN_MENU_TEXT, MAIN_MENU_KEYBOARD)
            return ConversationHandler.END

        # Saving chat id to `context.user_data` to use it in `job.context`
        context.user_data['chat_id'] = update.effective_chat.id
        self.dispatcher.persistence.update_user_data(
            user_id=update.message.from_user.id, data=context.user_data
        )

        return self.send_location_input(update, context)

    def send_location_input(self, update, context):
        # We ask user for city name because OpenWeather API recommends to get weather by city ID.
        # There are all available cities in assets/city.list.min.json.
        self.sender.message(update, LOCATION_INPUT_TEXT, LOCATION_INPUT_KEYBOARD)
        return self.LOCATION_INPUT

    def handle_location_input(self, update, context):
        location = update.message.location
        if location is not None:
            found_cities = cities.find_city_by_coords(location.longitude, location.latitude)
        else:
            found_cities = cities.find_city(update.message.text)

        if len(found_cities) == 0:
            return self.send_try_again(update)

        if len(found_cities) == 1:
            city = found_cities[0]
            return self.handle_city_set(update, context, city)

        context.chat_data["found_cities"] = found_cities
        return self.send_location_confirmation(update, found_cities[0])

    def send_location_confirmation(self, update, city):
        self.sender.message(
            update,
            LOCATION_CONFIRM_TEXT.format(cities.get_city_fullname(city)),
            LOCATION_CONFIRM_KEYBOARD,
        )
        return self.LOCATION_CONFIRM

    def send_try_again(self, update):
        self.sender.message(update, TRY_AGAIN_TEXT, LOCATION_INPUT_KEYBOARD)
        return self.LOCATION_INPUT

    def handle_location_confirm(self, update, context):
        answer = update.message.text.lower()
        if "yes" in answer:
            return self.handle_city_set(update, context, context.chat_data["found_cities"][0])
        elif "no" in answer:
            found_cities = context.chat_data["found_cities"]

            if len(found_cities) == 1:
                return self.send_try_again(update)

            context.chat_data["found_cities"].pop(0)
            return self.send_location_confirmation(update, context.chat_data["found_cities"][0])

    def handle_city_set(self, update, context, city):
        context.user_data["city"] = city
        self.dispatcher.persistence.update_user_data(
            user_id=update.message.from_user.id, data=context.user_data
        )
        self.sender.message(update, LOCATION_SET_TEXT.format(city["name"]), MAIN_MENU_KEYBOARD)
        return ConversationHandler.END
