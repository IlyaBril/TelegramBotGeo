from database.common.models import History
from telebot import types
from settings import SiteSettings
from site_API.core import site_api
from tg_API.core import bot
from tg_API.custom import Custom
from tg_API.high import High
from tg_API.history import BotHistory
from tg_API.low import Low


site = SiteSettings()
near_cities = site_api.get_cities_nearby()


class BotHelp():

    @bot.message_handler(commands=['help'])
    def help(message):
        bot.send_message(message.chat.id, 'Бот покажет ближайшие туристические объекты\n'
                                          '/low - ближайшие объекты\n'
                                          '/high - наиболее удаленные объеты\n'
                                          '/custom - объеты в диапазоне расстояния ОТ (метров) - ДО (метров)\n'
                                          '- Список категорий - введите "0" в командах выше.\n'
                                          '/history - последние 10 запросов')

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Привет! Бот покажет ближайшие туристические объекты.'
         + '\nВведите команду или /help')

        my_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_location = types.KeyboardButton(text='Обновить локацию', request_location=True)
        my_keyboard.add(button_location)

    @bot.message_handler(commands=['hello-world'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Привет! Бот покажет ближайшие туристические объекты.'
         + '\nВведите команду или /help')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def wrong_first_enter(message):
    if message.text.lower() == 'Привет':
        bot.send_message(message.chat.id, 'Привет - привет!')
        return
    else:
        bot.send_message(message.chat.id, 'Введите команду : \n/low\n/high\n/custom\n/history')
        bot.send_message(message.chat.id, 'или /help')
        return


class Help:
    pass


if __name__ == "__main__":
    BotHelp()
    Low()
    High()
    Custom()
    BotHistory()