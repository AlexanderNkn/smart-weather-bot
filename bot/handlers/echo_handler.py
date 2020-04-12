from telegram.ext import MessageHandler, Filters

from bot.handlers.handler import Handler


class EchoHandler(Handler):
    def __init__(self, dispatcher):
        self.handler = MessageHandler(Filters.text, self.handle)
        super().__init__(dispatcher)

    def handle(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
