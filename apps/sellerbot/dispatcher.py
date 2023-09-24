from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

from apps.sellerbot.main import *
from config.settings import BOT_TOKEN

bot: Bot = Bot(token=BOT_TOKEN)


def ready():
    pass
    # hostname = f'https://cashbek.omonatpay.uz/bot/'
    # print(f'setting MASTER webhook at {hostname}')
    # bot.set_webhook(hostname)


dispatcher: Dispatcher = Dispatcher(bot, None)

dispatcher.add_handler(CommandHandler(command='start', filters=Filters.chat_type.private, callback=start_handler))
dispatcher.add_handler(MessageHandler(filters=Filters.text & Filters.chat_type.private, callback=core))
