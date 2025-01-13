import telebot
from site_API.core import site


API = site.tg_api.get_secret_value()
URL = "https://api.telegram.org/MyGeobot_bot"

bot = telebot.TeleBot(API)
