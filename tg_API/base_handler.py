from telebot import TeleBot


class BaseHandler:
    "Main handler class"
    def __init__(self, bot: TeleBot):
        self.bot = bot
        self.register_handlers()

    def register_handlers(self):
        """Handlers registration method
        To be redefined in child class"""
        pass