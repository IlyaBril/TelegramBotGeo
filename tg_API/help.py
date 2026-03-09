from telebot import types
from tg_API.core import bot
from .base_handler import BaseHandler
from site_API.utils.models import user_settings, URLFilterUnit

url_filter = URLFilterUnit()

class BotHelp(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            chat_id = message.chat.id
            if chat_id not in user_settings:
                user_settings[chat_id] = url_filter

            self.start_message(chat_id)

            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_location = types.KeyboardButton(text='Обновить локацию', request_location=True)
            keyboard.add(button_location)
            self.bot.send_message(chat_id, text='Для работы необходимо обновить локацию нажав на кнопку внизу',
                                  reply_markup=keyboard)


        @self.bot.message_handler(commands=['help'])
        def help_command(message):
            self.start_message(message.chat_id)




    def start_message(self, chat_id):
        self.bot.send_message(chat_id, 'Бот покажет ближайшие туристические объекты в радиусе 5 км\n'
                                          '/search - ближайшие объекты\n'
                                          )
