from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

from apps.sellerbot.main import start_handler
from config.settings import BOT_TOKEN

bot: Bot = Bot(token=BOT_TOKEN)


def ready():
    pass
    hostname = f'https://ramazon88.jprq.live/bot/'
    print(f'setting MASTER webhook at {hostname}')
    bot.set_webhook(hostname)


dispatcher: Dispatcher = Dispatcher(bot, None)

dispatcher.add_handler(CommandHandler('start', start_handler))
dispatcher.add_handler(MessageHandler(Filters.text("asd"), start_handler))
