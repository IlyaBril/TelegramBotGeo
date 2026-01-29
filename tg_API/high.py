from database.common.models import db, History
from database.core import db_write
from .base_handler import BaseHandler
from tg_API.handle_location import Updated_location
from tg_API.places_list import category_list_str
from tg_API.tourist_places import TouristPlaces


class BotMostDistantPlaces(BaseHandler):
    def register_handlers(self):
        @self.bot.message_handler(commands=['high'])
        def high_execute(message):
            Updated_location.set_command('high_get_category')
            self.bot.send_message(message.chat.id, 'Введите название или номер категории\n'
                                              'Введите "0" для списка категорий')

        @self.bot.message_handler(func=lambda message: Updated_location.get_command() == 'high_get_category')
        def tourist_places_find(message):
            if message.text == '0':
                self.bot.send_message(message.chat.id, category_list_str)
                self.bot.send_message(message.chat.id, 'Введите категорию')
                db_write(db, History, {'request': "Список категорий из /high"})
            else:
                category = Updated_location.set_category(message.text)
                if category:
                    Updated_location.set_command('high_get_limit')
                    self.bot.send_message(message.chat.id, "Введите количество едениц категории (1 - 10).")

                else:
                    self.bot.send_message(message.chat.id,
                                     'Ошибка. Введите категорию поиска или номер категории,'
                                     '\nДля списка категорий введите "0"')


        @self.bot.message_handler(func=lambda message: Updated_location.get_command() == 'high_get_limit')
        def get_limit_func(message):
            limit = message.text
            if not limit.isdigit():
                self.bot.send_message(message.chat.id, "Что-то не так, попробуй ещё раз!")
                return
            elif 0 < int(limit) < 10:
                limit = int(limit)
                Updated_location.set_limit(100)
                Updated_location.set_command(None)
                receive_response = TouristPlaces().provide_response()
                receive_response = list(reversed(receive_response))
                receive_response = receive_response[0:limit+1]
                answer = TouristPlaces().print_properties(receive_response)
                self.bot.send_message(message.chat.id, answer)
                db_text = "Команда: /high\n" \
                          "Категория: {}\n" \
                          "Количество ед.: {}\n".format(Updated_location.get_category(), limit)
                db_write(db, History, {'request': db_text})
                return
            else:
                self.bot.send_message(message.chat.id, "Что-то не так! Введите число от 1 до 10!")
                return

            db_write(db, History, {'request': message.text})