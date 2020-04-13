from telegram.ext import MessageHandler, Filters

from bot.handlers.handler import Handler
from bot.keyboards import MAIN_MENU_KEYBOARD


class UnknownCommandHandler(Handler):
    def __init__(self, dispatcher):
        self.handler = MessageHandler(Filters.text, self.handle_unknown_command)

        super().__init__(dispatcher)

    def handle_unknown_command(self, update, context):
        self.sender.message(update, "Sorry, I can't understand you. Try again :)", MAIN_MENU_KEYBOARD)
