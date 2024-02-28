from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

from apps.minibot.main import *
from config.settings import MINIBOT

bot: Bot = Bot(token=MINIBOT)


def ready():
    pass
    # hostname = f'https://b8df-195-158-4-67.ngrok-free.app/minibot/'
    # print(f'setting MASTER webhook at {hostname}')
    # a = bot.set_webhook(hostname)
    # print(a)


dispatcher: Dispatcher = Dispatcher(bot, None)

dispatcher.add_handler(CommandHandler(command='start', filters=Filters.chat_type.private, callback=start_handler))
dispatcher.add_handler(MessageHandler(filters=Filters.all & Filters.chat_type.private, callback=core))
