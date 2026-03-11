import requests
from database.common.models import db, History
from database.core import db_write
from PIL import Image
from io import BytesIO
from site_API.utils.serializers import RequestSchema, MapPictureSchema, FinalSchema
from site_API.utils.site_api_handler import SiteApiInterface
from site_API.utils.models import user_settings
from site_API.core import url_places, map_static_url
from math import log
from .keyboards import category_buttons

from .base_handler import BaseHandler
from .keyboards import InlineKeyboard
from .states import CustomStates
from .help import BotHelp as bot_help


schema = RequestSchema()
static_map_schema = MapPictureSchema()
final_schema = FinalSchema()
tourist_places = SiteApiInterface.get_tourist_places()

class BotNealestPlaces(BaseHandler):
    """Handler returns nearest chosen tourists places"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot_help = bot_help

    def register_handlers(self):
        @self.bot.message_handler(content_types=['location'])
        def handle_location(message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            user_settings[user_id].lat = message.location.latitude
            user_settings[user_id].lon = message.location.longitude
            self.bot.send_message(chat_id, text='Локация обновлена')
            self.get_category(self, chat_id, user_id)

        @self.bot.message_handler(commands=['search'])
        def search(message):
            self.get_category(self, message.chat.id, message.from_user.id)

        @self.bot.callback_query_handler(func=lambda call: True, state=CustomStates.get_category)
        def get_nearest_places(call):
            """ Function requests returns message with nearest places by category
             and map picture with markers """

            chat_id = call.message.chat.id
            message_id = call.message.id
            user_id = call.from_user.id

            self.bot.answer_callback_query(call.id)
            self.bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                       text=f"Категория {category_buttons.get(call.data)} \n"
                                            f"Готовится ответ ... ")

            # Set category chosen by user
            user_settings[user_id].categories = call.data

            # Get row places list by category
            url_params = schema.dump(user_settings[user_id])
            headers = {}
            response = tourist_places("GET", url_places, headers=headers, timeout=5, params=url_params)
            if not hasattr(response, "status_code"):
                print('EMPTY')
                return return_or_repeat(chat_id, user_id)

            response = response.json()

            # Serialize to get markers JSON and request places map
            static_map_url_params = static_map_schema.dump(response)

            ## Add map center coordinates and customer position marker
            position_marker = {
                "lat": user_settings[user_id].lat,
                "lon": user_settings[user_id].lon,
                "type": "circle",
                "color": "#000099",
                "size": "22",
            }
            static_map_url_params["markers"].append(position_marker)

            # Add center coordinates to map
            static_map_url_params["center"] = {
                "lat": user_settings[user_id].lat,
                "lon": user_settings[user_id].lon,
            }


            ### Add zoom adjust function ###
            max_distance = max(map(lambda x: x['properties']['distance'], response['features']))
            zoom = log(8000000/max_distance, 2)
            print('max distance: ', max_distance/1000, "  ", zoom)
            static_map_url_params["zoom"] = zoom

            #Request and Send static map image to chat
            static_map_response = requests.request("POST", map_static_url, json=static_map_url_params)
            static_map_img_data = static_map_response.content
            static_map_image = Image.open(BytesIO(static_map_img_data))
            self.bot.send_photo(chat_id=chat_id, photo=static_map_image)

            # Get final answer with requested list of places
            places_list = final_schema.dump(response)
            self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=places_list, parse_mode='HTML')

            #Save request data to database
            db_write(db, History, {'request': places_list})
            self.bot.delete_state(user_id, chat_id)

            self.bot.send_message(chat_id=chat_id, text='Повторить запрос или вернуться на главную страницу?',
                                  reply_markup=InlineKeyboard.repeat())

        @self.bot.callback_query_handler(func=lambda call: call.data == 'repeat')
        def repeat(call):
            chat_id = call.message.chat.id
            message_id = call.message.id
            user_id = call.from_user.id
            self.bot.answer_callback_query(call.id)
            self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Возвращаемся")
            self.get_category(self, chat_id, user_id)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'return')
        def return_action(call):
            chat_id = call.message.chat.id
            user_id = call.message.from_user.id
            self.bot.answer_callback_query(call.id)
            self.bot.delete_state(user_id, chat_id)
            self.bot_help.start_message(self, chat_id)

        def return_or_repeat(chat_id, user_id):
            self.bot.delete_state(user_id, chat_id)
            self.bot.send_message(chat_id=chat_id, text='Объектов с запрошенными параметрами не найдено',
                                  )
            self.bot.send_message(chat_id=chat_id, text='Повторить запрос или вернуться на главную страницу?',
                                  reply_markup=InlineKeyboard.repeat())


        @self.bot.message_handler(commands=['cancel'])
        def cancel_command(message):
            user_id = message.from_user.id
            chat_id = message.chat.id
            self.bot.delete_state(user_id, chat_id)
            self.bot.send_message(chat_id, "cancel")


    @staticmethod
    def get_category(self, chat_id, user_id):
        """ Function requests category from user """

        print("get category")

        self.bot.set_state(user_id, CustomStates.get_category, chat_id)
        self.bot.send_message(chat_id, 'Выберите категорию',
                              reply_markup=InlineKeyboard.get_categoties())
