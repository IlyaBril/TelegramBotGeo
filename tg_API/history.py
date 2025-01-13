from database.common.models import db, History
from database.core import db_write, db_read
from settings import SiteSettings
from site_API.core import site_api, url, headers, params
from tg_API.core import bot

site = SiteSettings()
near_cities = site_api.get_cities_nearby()


class BotHistory():
    @bot.message_handler(commands=['history'])
    def history(message):
        retrieved = db_read(db, History, History.request)
        result = []
        for i in retrieved:
             result.append(i.request)

        result = result[-10:]
        result = "\n".join(result)
        bot.send_message(message.chat.id, result)


if __name__ == "__main__":
    BotHistory()