import telebot
from settings import site


API = site.tg_api.get_secret_value()
URL = ("https://api.telegram.org/MyGeoT"
       "bot_bot")

bot = telebot.TeleBot(API)