from tg_API.history import BotHistory
from tg_API.help import BotHelp
from tg_API.low import BotNealestPlaces
from tg_API.high import BotMostDistantPlaces
from tg_API.custom import BotCustomDistancePlaces
from tg_API.core import bot


history = BotHistory(bot)
nealest_places = BotNealestPlaces(bot)
most_distant_places = BotMostDistantPlaces(bot)
custom_distance_places = BotCustomDistancePlaces(bot)
help = BotHelp(bot)

if __name__ == "__main__":
    bot.polling(non_stop=True, interval=0)