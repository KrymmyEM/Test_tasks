from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from bot_elements.callback import ItemCallback

catalog_button = KeyboardButton(text='Каталог')
basket_button = KeyboardButton(text='Корзина')
faq_button = KeyboardButton(text='FAQ')
menu_keyboard = ReplyKeyboardBuilder()
menu_keyboard.row(catalog_button, basket_button, faq_button)

keyboard_inline_builder = InlineKeyboardBuilder

menu_catalog_builder = InlineKeyboardBuilder()
menu_catalog_builder.button(text="Добавить в корзину",
                                            callback_data=ItemCallback(action_type="add", count=1).pack())
menu_catalog_builder.button(text="Следующий товар", callback_data=ItemCallback(action_type="next").pack())

menu_catalog = menu_catalog_builder.as_markup()

menu_basket_item_builder = InlineKeyboardBuilder()
menu_basket_item_builder.button(text="Добавить в корзину",
                                callback_data=ItemCallback(action_type="add", count=1).pack())
menu_basket_item_builder.button(text="Убрать из корзины", callback_data=ItemCallback(action_type="del").pack())

menu_basket_item = menu_basket_item_builder.as_markup()

menu_basket_builder = ReplyKeyboardBuilder().button(text="Оформить заказ").button(text="/start")
menu_basket = menu_basket_builder.as_markup()

yes_no_keyboard = ReplyKeyboardBuilder().add(KeyboardButton(text="Да"), KeyboardButton(text="Нет")).as_markup()
