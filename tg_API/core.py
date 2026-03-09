import telebot
from settings import site
from telebot.storage import StateMemoryStorage
from telebot import custom_filters


state_storage = StateMemoryStorage()
API = site.tg_api.get_secret_value()
URL = ("https://api.telegram.org/MyGeoT"
       "bot_bot")

bot = telebot.TeleBot(API, state_storage=state_storage)
bot.add_custom_filter(custom_filters.StateFilter(bot))
