class MessageSender:
    """
    Takes the bot object and provides `message` method
    which send messages with passed text and keyboard.
    """

    def __init__(self, bot):
        self.bot = bot

    def message(self, update, text, keyboard):
        # Parse chat_id from `update` object
        chat_id = update.effective_chat.id
        return self.bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
