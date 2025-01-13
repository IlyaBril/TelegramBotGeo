from database.common.models import db, History
from database.core import db_write, db_read
from tg_API.core import bot
from tg_API.handle_location import CustomerLocation, Updated_location
from tg_API.places_list import category_list_str
from tg_API.tourist_places import TouristPlaces


class Custom():

    def delete_low_radius(self, response: dict, min_distance: int) -> dict:
        result = []
        for i in response:

            if int(i['properties']['distance']) > min_distance:
                result.append(i)


        return result

    @bot.message_handler(commands=['custom'])
    def custom_execute(message):
        Updated_location.set_command('custom_get_category')
        bot.send_message(message.chat.id, 'Введите название или номер категории\n'
                                          'Введите "0" для списка категорий')
        return

    @bot.message_handler(func=lambda message: Updated_location.get_command() == 'custom_get_category')
    def tourist_places_find(message):
        if message.text == '0':
            bot.send_message(message.chat.id, category_list_str)
            bot.send_message(message.chat.id, 'Введите категорию')
            db_write(db, History, {'request': "Список категорий из /custom"})
        else:
            category = Updated_location.set_category(message.text)
            if category:
                Updated_location.set_command('radius_min')
                bot.send_message(message.chat.id,
                                 "Введите значение минимального радиуса поиска в метрах от (1 - 5000м)")
            else:
                bot.send_message(message.chat.id,
                                 'Ошибка. Введите категорию поиска или номер категории,'
                                 '\nДля списка категорий введите "0"')

    @bot.message_handler(func=lambda message: Updated_location.get_command() == 'radius_min')
    def set_custom_min(message):
        if not message.text.isdigit():
            bot.send_message(message.chat.id, "Что-то не так, попробуй ещё раз!")
            return
        else:
            result = Updated_location.set_radius_min(int(message.text))
            if result:
                Updated_location.set_command('radius_max')
                bot.send_message(message.chat.id, "Принято")
                bot.send_message(message.chat.id,
                                 "Введите значение максимального радиуса поиска"
                                 " в метрах от ({} - 5000м)".format(Updated_location.get_radius_min()))
                return
            else:
                bot.send_message(message.chat.id, "Что-то не так, попробуй ещё раз! 2")
                return

    @bot.message_handler(func=lambda message: Updated_location.get_command() == 'radius_max')
    def set_custom_max(message):
        if not message.text.isdigit():
            bot.send_message(message.chat.id, "Что-то не так, попробуй ещё раз!")
            return
        else:
            result = Updated_location.set_radius_max(int(message.text))
            if result:
                Updated_location.set_command('high_set_limit')
                bot.send_message(message.chat.id, "Принято")
                bot.send_message(message.chat.id,
                                 "Введите количество едениц категории (1 - 10).")
                return
            else:
                bot.send_message(message.chat.id, "Что-то не так, попробуй ещё раз!")
                return

    @bot.message_handler(func=lambda message: Updated_location.get_command() == 'high_set_limit')
    def set_custom_max(message):
        limit = message.text
        if not limit.isdigit():
            bot.send_message(message.chat.id, "Что-то не так, попробуй ещё раз!")
            return
        elif 0 < int(limit) < 10:
            limit = int(limit) #Запрашиваем количество ед. категорий
            Updated_location.set_limit(100)  #Но API запрашиваем по-максимуму, чтобы потом взять наиболее удаленные
            Updated_location.set_command(None)
            receive_response = TouristPlaces().provide_response()
            receive_response = Custom().delete_low_radius(receive_response, int(Updated_location.get_radius_min()))
            receive_response = receive_response[:limit + 1]
            mess = TouristPlaces().print_properties(receive_response)
            bot.send_message(message.chat.id, mess)
            db_text = "Команда: /custom\n" \
                      "Категория: {}\n" \
                      "Мин. расстояние: {}\n" \
                      "Макс. расстояние: {}\n" \
                      "Количество ед.: {}\n".format(Updated_location.get_category(),
                                                    Updated_location.get_radius_min(),
                                                    Updated_location.get_radius_max(),
                                                    limit)
            db_write(db, History, {'request': db_text})
            return
        else:
            bot.send_message(message.chat.id, "Что-то не так! Введите число от 1 до 10!")
            return


if __name__ == "__main__":
    Custom()
