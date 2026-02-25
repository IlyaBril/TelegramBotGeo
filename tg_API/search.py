from database.common.models import db, History
from database.core import db_write
from tg_API.handle_location import Updated_location
from tg_API.tourist_places import TouristPlaces
from .base_handler import BaseHandler
from .keyboards import InlineKeyboard
import requests
from PIL import Image
from io import BytesIO
from site_API.utils.serializers import RequestSchema, FeaturesSchema, FinalSchema
from site_API.utils.site_api_handler import SiteApiInterface
from site_API.core import url_geo, headers_geo, url_geo_rev, url_places

tourist_places = SiteApiInterface.get_tourist_places()

from site_API.utils.serializers import bot_response

schema = RequestSchema()
picture_schema = FeaturesSchema()
final_schema = FinalSchema()
get_tourist_places = TouristPlaces

class BotNealestPlaces(BaseHandler):
    """Handler returns nealest choosen tourists places"""

    def register_handlers(self):
        def get_category(message):
            self.bot.send_message(message.chat.id, 'Выберите категорию',
                                  reply_markup=InlineKeyboard.get_categoties())
            Updated_location.set_command('get_category')


        @self.bot.message_handler(commands=['search'])
        def low_execute(message):
            get_category(message)

        @self.bot.callback_query_handler(func=(lambda call: call) and (lambda message: Updated_location.get_command() == 'get_category'))
        def get_nealest_places(call):

            """ Function requests category from user """

            chat_id = call.message.chat.id
            message_id = call.message.id
            self.bot.answer_callback_query(call.id)
            self.bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                       text="Готовится ответ ... ")

            bot_response.categories = call.data

            #Get tourists places
            url_params = schema.dump(bot_response)
            headers = {}
            print("url params", url_params)
            response = tourist_places("GET", url_places, headers=headers, timeout=5, params=url_params)

            response = response.json()

            # Send picture
            # Serialize to marker JSON
            url_params = picture_schema.dump(response)
            picture_url = "https://maps.geoapify.com/v1/staticmap?apiKey=3b6995fba84146909e2b65f0f8efacaf"
            map_response = requests.request("POST", picture_url, json=url_params)
            img_data = map_response.content
            image = Image.open(BytesIO(img_data))
            self.bot.send_photo(chat_id=chat_id, photo=image)

            # Get list of places
            places_list = final_schema.dump(response)
            self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=places_list)


            #Save request data to database
            db_write(db, History, {'request': places_list})
            Updated_location.set_command('choose_action')
            self.bot.send_message(chat_id=chat_id, text='Повторить запрос или вернуться на главную страницу?',
                                  reply_markup=InlineKeyboard.repeat())

        @self.bot.callback_query_handler(func=lambda call: call.data == 'repeat')
        def repeat(call):
            chat_id = call.message.chat.id
            message_id = call.message.id
            self.bot.answer_callback_query(call.id)
            self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Возвращаемся")
            Updated_location.set_command(None)
            get_category(call.message)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'return')
        def return_action(call):
            chat_id = call.message.chat.id
            message_id = call.message.id
            self.bot.answer_callback_query(call.id)
            text = 'Бот покажет ближайшие туристические объекты\n'\
                   '/search - ближайшие объекты\n'\
                   '/settings - настройки\n'\
                   '/history - последние 10 запросов'

            self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
            Updated_location.set_command(None)


        #test
        @self.bot.message_handler(commands=['pic'])
        def pic_execute(message):
            #url="https://api-maps.yandex.ru/services/constructor/1.0/static/?um=constructor%3A3GbTRNmB8Pz5lk_2mngDAxWGCr7ZhJ8L&amp;lang=ru_RU"
            #url = "https://maps.geoapify.com/v1/staticmap?style=osm-bright&width=600&height=400&center=lonlat:-122.304378,47.526022&zoom=14&marker=lonlat:-122.30021521160944,47.52683340049401;color:%23ff0000;size:42|lonlat:-122.30622335980286,47.523645683495744;color:%23ff0000;size:42|lonlat:-122.30609461377031,47.52761581051092;color:%23ff0000;size:42|lonlat:-122.30004355023252,47.5216749979148;color:%23ff0000;size:42|lonlat:-122.29691073010325,47.525674253090216;color:%23ff0000;size:42|lonlat:-122.30214640210025,47.52492079354127;color:%23ff0000;size:42&apiKey=3b6995fba84146909e2b65f0f8efacaf"
            #self.bot.send_photo(chat_id=message.chat.id, photo=url)
            url2 = "https://maps.geoapify.com/v1/staticmap?apiKey=3b6995fba84146909e2b65f0f8efacaf"
            params = {
                    "style": "osm-bright",
                    "scaleFactor": 2,
                    "width": 600,
                    "height": 400,
                    "center": {
                        "lat": 47.527906,
                        "lon": -122.300215
                    },
                    "zoom": 14,
                    "markers": [
                        {
                            "lat": 47.52492079354127,
                            "lon": -122.30214640210025,
                            "color": "#ff0000",
                            "size": "42",
                            "text": "2",
                            "contentsize": "22",
                        },
                        {
                            "lat": 47.52819536596189,
                            "lon": -122.30313345501769,
                            "color": "#ff0000",
                            "size": "42",
                            "text": "3",
                            "contentsize": "22",
                        },
                        {
                            "lat": 47.52776069997742,
                            "lon": -122.29476496289027,
                            "color": "#ff0000",
                            "size": "42",
                            "text": "1",
                            "contentsize" : "22",
                        }
                    ]
                }

            from site_API.utils.models import params_2
            response = requests.request("POST", url2, json=params_2)
            #print(response)
            img_data = response.content
            image = Image.open(BytesIO(img_data))
            self.bot.send_photo(chat_id=message.chat.id, photo=image)
