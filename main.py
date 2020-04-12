from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from bot.config import BOT_TOKEN

if __name__ == '__main__':
    def echo(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


    def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hi!")


    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    updater.idle()
