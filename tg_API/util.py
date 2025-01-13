from tg_API.low import Low
from tg_API.core import bot
from tg_API.custom import Custom
from tg_API.handle_location import BotLocation
from tg_API.help import BotHelp
from tg_API.high import High
from tg_API.history import BotHistory
from tg_API.tourist_places import TouristPlaces


def _low(message):
    Low.low(message)


def _start_message(message):
    BotHelp.start_message(message)


def _handle_location(message):
    BotLocation.handle_location(message)


def _history(message):
    BotHistory.history(message)


def _help(message):
    BotHelp.help(message)


def _tourist_places(message):
    TouristPlaces.tourist_places_find(message)


def _custom(message):
    Custom.custom(message)


def _high(message):
    High.high(message)


class MyBot():

    @staticmethod
    def low():
        return _low()

    @staticmethod
    def handle_location(message):
        return _handle_location()

    @staticmethod
    def history():
        return _history()

    @staticmethod
    def start_message(message):
        return _start_message()

    @staticmethod
    def help():
        return _help()

    @staticmethod
    def tourist_places():
        return _tourist_places()

    @staticmethod
    def custom():
        return _custom()

    @staticmethod
    def high():
        return _high()

    @staticmethod
    def bot_start():
        bot.polling(non_stop=True, interval=0)



if __name__ == "__main__":
    MyBot()
    _custom()
    _low()
    _high()
    _handle_location()
    _start_message()
    _history()
    _help()
    _tourist_places()






