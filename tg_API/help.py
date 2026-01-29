from telebot import types
from tg_API.core import bot
from .base_handler import BaseHandler


class BotHelp(BaseHandler):
    def register_handlers(self):
        @self.bot.message_handler(commands=['help'])
        def help(message):
            bot.send_message(message.chat.id, 'Бот покажет ближайшие туристические объекты\n'
                                              '/low - ближайшие объекты\n'
                                              '/high - наиболее удаленные объеты\n'
                                              '/custom - объеты в диапазоне расстояния ОТ (метров) - ДО (метров)\n'
                                              '- Список категорий - введите "0" в командах выше.\n'
                                              '/history - последние 10 запросов')

        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            bot.send_message(message.chat.id, 'Привет! Бот покажет ближайшие туристические объекты.'
             + '\nВведите команду или /help')

            my_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_location = types.KeyboardButton(text='Обновить локацию', request_location=True)
            my_keyboard.add(button_location)

        @self.bot.message_handler(commands=['hello-world'])
        def start_message(message):
            bot.send_message(message.chat.id, 'Привет! Бот покажет ближайшие туристические объекты.'
             + '\nВведите команду или /help')


        @self.bot.message_handler(func=lambda message: True, content_types=['text'])
        def wrong_first_enter(message):
            if message.text.lower() == 'Привет':
                bot.send_message(message.chat.id, 'Привет - привет!')
                return
            else:
                bot.send_message(message.chat.id, 'Введите команду : \n/low\n/high\n/custom\n/history')
                bot.send_message(message.chat.id, 'или /help')