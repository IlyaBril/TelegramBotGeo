from telebot.handler_backends import State, StatesGroup

# Define states
class CustomStates(StatesGroup):
    get_category = State()
    choose_action = State()
    whatsup = State()
