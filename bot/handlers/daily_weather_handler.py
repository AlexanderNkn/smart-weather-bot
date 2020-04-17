from telegram.ext import MessageHandler, Filters, ConversationHandler
import datetime as dt

from bot.handlers.handler import Handler
from bot.utils.timezone import get_timezone_by_coords, parse_timezone
from bot.utils.weather import get_city_weather
from bot.texts import TIME_INPUT_TEXT, TIME_SET_TEXT, DAILY_WEATHER_TEXT, UNKNOWN_ERROR_TEXT
from bot.keyboards import MAIN_MENU_KEYBOARD, ONLY_TIME_INPUT_KEYBOARD, DELETE_CURRENT_SUB_KEYBOARD


def _keyboard(context):
    """Return keyboard that depends on the availability of user job"""
    if context.user_data.get('daily_job_context') is not None:
        return DELETE_CURRENT_SUB_KEYBOARD
    return ONLY_TIME_INPUT_KEYBOARD


def _find_user_jobs(chat_id, job_queue):
    return filter(lambda j: j.context.get('chat_id') == chat_id, job_queue.jobs())


class DailyWeatherHandler(Handler):
    # States
    TIME_INPUT = 1

    def __init__(self, dispatcher):
        self.handler = ConversationHandler(
            entry_points=[
                MessageHandler(Filters.regex(r"^.*(?i)daily weather notify(?-i:)"), self.send_time_input)
            ],
            states={
                self.TIME_INPUT: [
                    MessageHandler(Filters.regex(r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"), self.handle_time_input),
                    MessageHandler(
                        Filters.regex(r"^.*(?i)cancel my current subscription(?-i:)"),
                        self.handle_delete_current_subscription
                    ),
                    MessageHandler(Filters.text, self.handle_invalid_time)
                ]
            },
            fallbacks=[],
            allow_reentry=True
        )

        super().__init__(dispatcher)

        self._start_daily_jobs()

    def send_time_input(self, update, context):
        city = context.user_data.get('city')
        if city is None:
            self.sender.message(update, 'Please, use command `/start` to restart me.', MAIN_MENU_KEYBOARD)
            return ConversationHandler.END
        self.sender.message(update, TIME_INPUT_TEXT, _keyboard(context))
        return self.TIME_INPUT

    def handle_time_input(self, update, context):
        city_coords = context.user_data['city']['coord']
        longitude = city_coords['lon']
        latitude = city_coords['lat']
        timezone_object = get_timezone_by_coords(longitude, latitude)

        if not timezone_object:
            self.sender.message(update, UNKNOWN_ERROR_TEXT, MAIN_MENU_KEYBOARD)
            return ConversationHandler.END

        timezone, zone_name = parse_timezone(timezone_object)
        time = dt.datetime.strptime(update.message.text, "%H:%M").time().replace(tzinfo=timezone)

        # Delete current user jobs
        user_chat_id = update.effective_chat.id
        for job in _find_user_jobs(user_chat_id, context.job_queue):
            job.schedule_removal()

        # Make a new job
        job_context = {
            "chat_id": update.effective_chat.id,
            "city": context.user_data['city'],
        }
        context.user_data.update({'daily_job_context': job_context})
        context.user_data.update({"daily_job_time": time})
        self.dispatcher.persistence.update_user_data(
            user_id=update.message.from_user.id, data=context.user_data
        )
        self.dispatcher.persistence.flush()
        context.job_queue.run_daily(self.send_daily_weather, time, context=job_context)

        self.sender.message(
            update,
            TIME_SET_TEXT.format(time.strftime('%H:%M'), zone_name),
            MAIN_MENU_KEYBOARD
        )
        return ConversationHandler.END

    def handle_invalid_time(self, update, context):
        self.sender.message(update, "Sorry, I can't understand that time, please try again", _keyboard(context))
        return self.TIME_INPUT

    def handle_delete_current_subscription(self, update, context):
        if context.user_data.get('daily_job_context') is None:
            self.sender.message(update, "You don't have any subscriptions.", ONLY_TIME_INPUT_KEYBOARD)
            return self.TIME_INPUT

        user_chat_id = update.effective_chat.id
        for job in _find_user_jobs(user_chat_id, context.job_queue):
            job.schedule_removal()
        context.user_data['daily_job_context'] = None
        context.user_data['daily_job_time'] = None
        self.dispatcher.persistence.update_user_data(
            user_id=update.message.from_user.id, data=context.user_data
        )
        self.dispatcher.persistence.flush()

        self.sender.message(update, "Subscription canceled successfully!", MAIN_MENU_KEYBOARD)
        return ConversationHandler.END

    def send_daily_weather(self, context):
        city_id = context.job.context['city']['id']
        weather = get_city_weather(city_id, DAILY_WEATHER_TEXT)
        if weather is None:
            self.sender.message(context.job.context, UNKNOWN_ERROR_TEXT, MAIN_MENU_KEYBOARD)
            return
        self.sender.job_context_message(context.job.context, weather, MAIN_MENU_KEYBOARD)

    def _start_daily_jobs(self):
        job_queue = self.dispatcher.job_queue
        for user in self.dispatcher.persistence.get_user_data().values():
            job_context = user.get('daily_job_context')
            if job_context is None:
                continue
            daily_time = user.get('daily_job_time')
            job_queue.run_daily(self.send_daily_weather, daily_time, context=job_context)
