from database.common.models import db, History
from database.core import db_read
from .base_handler import BaseHandler


class BotHistory(BaseHandler):
    """ Handler returns 10 last requests """

    def register_handlers(self):
        @self.bot.message_handler(commands=['history'])
        def history(message):
            retrieved = db_read(db, History, History.request)
            result = []
            for i in retrieved:
                 result.append(i.request)

            result = result[-10:]
            result = "\n".join(result)
            self.bot.send_message(message.chat.id, result)