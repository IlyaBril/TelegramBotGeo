import re
from settings import site
from tg_API.core import bot
from site_API.utils.models import user_settings

class CustomerLocation:
    def __init__(
            self,
            command=None, category=None,
    ):
        self._command = command

    def set_command(self, command):
        self._command = command

    def get_command(self):
        return self._command


Updated_location = CustomerLocation()


class BotLocation():

    @bot.message_handler(content_types=['location'])
    def handle_location(message):
        chat_id = message.chat.id
        user_settings[chat_id].lat = message.location.latitude
        user_settings[chat_id].lon = message.location.longitude
        bot.send_message(chat_id, 'Бот покажет ближайшие туристические объекты\n'
                                          '/search - ближайшие объекты\n'
                                          '/settings - настройки\n'
                                          '/history - последние 10 запросов')
