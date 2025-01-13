import requests
from tg_API.handle_location import Updated_location
from settings import SiteSettings
from site_API.core import site_api, url_geo, headers_geo, url_geo_rev

site = SiteSettings()
near_cities = site_api.get_cities_nearby()
tourist_places = site_api.get_tourist_places()


class TouristPlaces():

    def reverse_geo(self, lat, lon):
        # Ф-ция принимает на вход координаты, возвращает адрес.
        # Нужна, так как в response нет полного адреса объекта
        url_geo_rev_2 = url_geo_rev + "lat=" + str(lat) + "&lon=" + str(lon)
        resp = requests.get(url_geo_rev_2, headers=headers_geo)
        resp = resp.json()['results'][0]['formatted']
        return resp

    def print_properties(self, response: list) -> str:
        # Ф-ция принимает на вход json твет (response)
        # по списоку категорий (args) возвращает ответ
        args = ['name', 'address', 'distance']
        category = {'name': 'Название', 'address': 'Адрес', 'distance': 'Расстояние'}
        answer = ""

        for key in response:
            lat = key['properties']['lat']
            lon = key['properties']['lon']
            # по координатам получаем полный адрес
            key['properties']['address'] = self.reverse_geo(lat, lon)
            for i in args:
                try:
                    answer = answer + str(category[i]) + ': ' + str(key['properties'][i]) + '\n'
                except Exception:  # Если в response нет такой категории, присваиваем  "-"
                    answer = answer + str(category[i]) + ': ' + ' -  \n'
            answer = answer + '\n'
        return answer

    def provide_response(self) -> str:
        # запрашивает ответ от API сайта
        headers_geo["Accept"] = "application/json"
        location = Updated_location.get_location()
        location = str(location[1]) + ',' + str(location[0])
        radius = Updated_location.get_radius_max()
        categories = Updated_location.get_category()
        limit = Updated_location.get_limit()
        lang = "ru"
        url_geo2 = "{}{},{}&categories={}&limit={}&lang={}&bias=proximity:{}".format(
            url_geo, location, radius, categories, limit, lang, location)
        print(url_geo2)
        response = tourist_places("GET", url_geo2, headers_geo, timeout=5)
        response = response.json()["features"]
        return response


if __name__ == "__main__":
    TouristPlaces()