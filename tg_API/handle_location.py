import re
from settings import SiteSettings
from site_API.core import site_api
from tg_API.core import bot
from tg_API.places_list import category_list, category_list_eng

site = SiteSettings()
near_cities = site_api.get_cities_nearby()


class CustomerLocation():
    def __init__(
            self, lat=55.755864, lon=37.617698,
            radius_min=0, radius_max=5000, limit=5,
            command=None, category=None):
        self._customer_lat = lat
        self._customer_lon = lon
        self._radius_min = radius_min
        self._radius_max = radius_max
        self._limit = limit
        self._command = command
        self._category = category

    def set_location(self, lat, lon):
        self._customer_lat = lat
        self._customer_lon = lon

    def get_location(self):
        return self._customer_lat, self._customer_lon

    def set_radius_min(self, radius_min):
        try:
            if 0 < radius_min < 5000:
                self._radius_min = radius_min
                result = True
            else:
                result = False
        except Exception as a:
            result = False
        return result

    def get_radius_min(self):
        return self._radius_min

    def set_radius_max(self, radius_max):
        try:
            if self.get_radius_min() < radius_max < 5000:
                self._radius_max = radius_max
                result = True
            else:
                result = False
        except Exception:
            result = False
        return result

    def get_radius_max(self):
        return self._radius_max

    def set_limit(self, limit):
        self._limit = limit

    def get_limit(self):
        return self._limit

    def set_command(self, command):
        self._command = command

    def get_command(self):
        return self._command

    def set_category_eng(self, category):
        # Функция проеверяет запрос категории на правильность
        # Возвращает категорию в зависимости от формата запроса (слово или цифра)
        # Категория по названию
        if category.lower() in category_list_eng[0:int(len(category_list_eng) - 1)]:
            self._category = category.lower()
            result = True

        # Категория по номеру
        elif re.search(r'\b\d{1,2}\b', category) != None and int(category) > 0 and int(category) <= (
                    len(category_list_eng) - 1):
            self._category = str(category_list_eng[int(category) - 1])
            result = True
        else:
            result = False
        return result

    def set_category(self, category):
        # Функция проеверяет запрос категории на правильность
        # Возвращает категорию в зависимости от формата запроса (слово или цифра)
        # Категория по названию
        category = category.lower()
        checklist_ru = [i[1].lower() for i in category_list]
        if category.lower() in checklist_ru:
            category = checklist_ru.index(category)
            self._category = category_list[category][0]
            result = True

        # Категория по номеру
        elif re.search(r'\b\d{1,2}\b', category) != None and int(category) > 0 and int(category) <= (
                len(category_list) - 1):
            self._category = str(category_list[int(category) - 1][0])
            result = True
        else:
            result = False
        return result

    def get_category(self):
        return self._category




Updated_location = CustomerLocation()


class BotLocation():

    @bot.message_handler(content_types=['location'])
    def handle_location(message):
        Updated_location.set_location(message.location.latitude, message.location.longitude)


if __name__ == "__main__":
    BotLocation()
    CustomerLocation()
