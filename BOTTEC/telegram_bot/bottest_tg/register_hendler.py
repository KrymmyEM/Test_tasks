from init_base import dispatcher
from aiogram.dispatcher import filters
from handlers import user


def register_hadlers_user(dispatcher: Dispatcher):
    dispatcher.register_message_handler(user.command_start, commands=['start'])
    dispatcher.register_message_handler(user.catalod_start, filters.Text(ignore_case = "каталог"))
    dispatcher.register_callback_query(user.get_category, filters.Text())
    dispatcher.register_message_handler(user.basket_start, filters.Text(ignore_case = "корзина"))
    dispatcher.register_message_handler(user.faq_start, filters.Text(ignore_case = "faq"))

