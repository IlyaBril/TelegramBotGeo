from tg_API.history import BotHistory
from tg_API.help import BotHelp
from tg_API.search import BotNealestPlaces
from tg_API.core import bot


history = BotHistory(bot)
nealest_places = BotNealestPlaces(bot)
help = BotHelp(bot)

if __name__ == "__main__":
    bot.polling(non_stop=True, interval=0)
