from pyexpat import features

import requests
from tg_API.handle_location import Updated_location
from site_API.core import url_geo, headers_geo, url_geo_rev, url_places
from site_API.utils.site_api_handler import SiteApiInterface
from site_API.utils.serializers import FeaturesSchema, FinalSchema

tourist_places = SiteApiInterface.get_tourist_places()
features_schema = FeaturesSchema()
final_schema = FinalSchema()

class TouristPlaces:

    @staticmethod
    def print_properties(response: list) -> str:
        """
        Ф-ция принимает на вход json ответ (response)
        по списоку категорий (args) возвращает ответ для бота
        """

        fields = {'name': 'Название', 'formatted': 'Адрес', 'distance': 'Расстояние'}
        answer = ""
        place_id = 0

        for place in response:
            answer = answer + str(place_id + 1) + "."
            place_id += 1
            for field_key, value in fields.items():
                try:
                    answer = answer + str(fields[field_key]) + ': ' + str(place['properties'][field_key]) + '\n'
                except Exception:  # Если в response нет такой категории, присваиваем  "-"
                    answer = answer + str(fields[field_key]) + ': ' + ' -  \n'
            answer = answer + '\n'
        return answer

    @staticmethod
    def provide_response(params: dict) -> str:
        """
        Function performs GET request to url and returns text answer with places
        :param params:
        :return:
        """

        headers = {}
        response = tourist_places("GET", url_places, headers=headers, timeout=5, params=params)

        if hasattr(response, "status_code"):
            response = response.json()
            #print('provide response', response)

            # Получаем адреса объектов по координатам и говоим финальный ответ

            text2 = final_schema.dump(response)
            print('text 2 ', text2)

        else:
            return "Объектов с запрошенными параметрами не найдено"
        return text2
