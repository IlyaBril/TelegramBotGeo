from database.common.models import db, History
from database.core import db_write
from tg_API.handle_location import Updated_location
from tg_API.tourist_places import TouristPlaces
from .base_handler import BaseHandler
from .keyboards import InlineKeyboard


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

            Updated_location.set_category_direct(call.data)

            # Получаем список объектов
            answer = TouristPlaces().provide_response()

            self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=answer)

            #Save request data to database

            places_qty = Updated_location.get_limit()
            db_text = "Команда: /low\nКатегория: {}" \
                      "\nКоличество ед.:{}\n".format(Updated_location.get_category(), places_qty)
            db_write(db, History, {'request': db_text})
            Updated_location.set_command('choose_action')
            self.bot.send_message(chat_id=chat_id, text='Повторить запрос или вернуться на главную страницу?',
                                  reply_markup=InlineKeyboard.repeate())

        @self.bot.callback_query_handler(func=lambda call: call.data == 'repeate')
        def repeate(call):
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
