from telebot import types

category_buttons_2  = [['entertainment.museum', 'Музеи'],
                         ['national_park', 'Парки'],
                         ['entertainment', 'Развлечения'],
                         ['catering.restaurant', 'Рестораны'],
                         ['catering.food_court', 'Фудкорты'],
                         ['leisure.picnic', 'Места для пикника'],
                         ['accommodation', 'Гостинницы'],
                         ['parking', 'Парковки'],
                         ['public_transport', 'Транспорт'],
                         ['beach', 'Пляжи'],
                         ['amenity.toilet', 'Туалет'],
                      ['/help', 'help']
                      ]

category_buttons  = {
    'entertainment.museum': 'Музеи',
    'national_park': 'Парки',
    'entertainment': 'Развлечения',
    'catering.restaurant': 'Рестораны',
    'catering.food_court': 'Фудкорты',
    'leisure.picnic': 'Места для пикника',
    'accommodation': 'Гостинницы',
    'parking': 'Парковки',
    'public_transport': 'Транспорт',
    'beach': 'Пляжи',
    'amenity.toilet': 'Туалет',
    '/help': 'help',
}


class InlineKeyboard:
    @staticmethod
    def get_categoties():
        markup = types.InlineKeyboardMarkup(row_width=2)
        buttons  = [['entertainment.museum', 'Музеи'],
                         ['national_park', 'Парки'],
                         ['entertainment', 'Развлечения'],
                         ['catering.restaurant', 'Рестораны'],
                         ['catering.food_court', 'Фудкорты'],
                         ['leisure.picnic', 'Места для пикника'],
                         ['accommodation', 'Гостинницы'],
                         ['parking', 'Парковки'],
                         ['public_transport', 'Транспорт'],
                         ['beach', 'Пляжи'],
                         ['amenity.toilet', 'Туалет'],
                      ['/help', 'help']
                      ]

        buttons = category_buttons

        buttons = [types.InlineKeyboardButton(text, callback_data=data)
                   for data, text in buttons.items() ]
        markup.add(*buttons)
        return markup

    @staticmethod
    def repeat():
        markup = types.InlineKeyboardMarkup(row_width=2)
        buttons = [
            ('repeat', 'Повторить'),
            ('return', 'Меню'),
                   ]
        buttons = [types.InlineKeyboardButton(text, callback_data=data)
                   for data, text in buttons]
        markup.add(*buttons)
        return markup
