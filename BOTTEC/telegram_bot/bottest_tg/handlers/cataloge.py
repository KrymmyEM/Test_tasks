import pathlib
import types

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from pydantic import ValidationError
from sqlalchemy import select
from aiogram import filters, types

from handlers.basket import basket_main
from init_base import bot, async_session, media_dir
from models.base_models import Categories, SubCategories, Items, Users, Baskets, BasketItems
from handlers import checkers
from bot_elements.callback import CatalogeCallBack, ItemCallback
from bot_elements.states import GetItem
from bot_elements.keyboards import keyboard_inline_builder, menu_catalog, yes_no_keyboard, menu_keyboard
from services.mini_services import log_info

catalog_router = Router(name="cataloge")


@catalog_router.message(F.text.lower() == "каталог")
@checkers.control_user
async def catalog_main(message: types.Message, state: FSMContext, **kwargs):
    log_info(f"User {message.from_user.id}| check catalog")
    db = async_session()
    result = await db.execute(select(Categories))
    local_builder = keyboard_inline_builder()
    for category in result.scalars():
        local_builder.button(text=category.name,
                                      callback_data=CatalogeCallBack(type_cat="base", id_cat=category.id).pack())

    await db.close()

    local_builder.adjust(4)
    await state.set_state(GetItem.get_sub_category)
    await message.answer("Выберите категорию", reply_markup=local_builder.as_markup())


@catalog_router.callback_query(CatalogeCallBack.filter(F.type_cat == "base"), GetItem.get_sub_category)
async def get_subcategory(query: types.CallbackQuery, state: FSMContext, callback_data: CatalogeCallBack):
    log_info(f"User {query.from_user.id}| check sub cetegory")
    db = async_session()

    result = await db.execute(select(Users).where(Users.tg_id == query.from_user.id))
    user = result.scalar_one_or_none()
    result = await db.execute(select(Baskets).where(Baskets.user_id == user.id).where(Baskets.sell == False))
    basket = result.scalar_one_or_none()
    await state.set_data({"category_id": callback_data.id_cat, "basket_id": basket.id})
    result = await db.execute(select(SubCategories).where(SubCategories.category_id == callback_data.id_cat))

    local_builder = keyboard_inline_builder()
    for sub_category in result.scalars():
        local_builder.button(text=sub_category.name,
                             callback_data=CatalogeCallBack(type_cat="sub", id_cat=sub_category.id).pack())

    await db.close()

    local_builder.adjust(4)
    await state.set_state(GetItem.select_item)
    await query.message.edit_text("Выберите подкатегорию", reply_markup=local_builder.as_markup())


@catalog_router.callback_query(CatalogeCallBack.filter(F.type_cat == "sub"), GetItem.select_item)
@catalog_router.callback_query(ItemCallback.filter(F.action_type == "next"), GetItem.select_item)
async def show_item(query: types.CallbackQuery, callback_data: CatalogeCallBack | ItemCallback, state: FSMContext):
    db = async_session()
    data_callback_type = type(callback_data)
    if data_callback_type == CatalogeCallBack:
        await state.update_data({"sub_category_id": callback_data.id_cat,
                                 "selected_item_id": -1})

    state_data = await state.get_data()
    subcategory_id = state_data.get('sub_category_id')
    selected_item_id = state_data.get('selected_item_id')
    log_info(f"User {query.from_user.id}| waching items {subcategory_id=}, {selected_item_id=}")
    result = await db.execute(select(Items)
                              .where(Items.sub_category_id == subcategory_id)
                              .where(Items.id > selected_item_id)
                              .where(Items.count > 0))



    item = result.scalars().first()
    if item is None:
        result = await db.execute(select(Items)
                                  .where(Items.sub_category_id == subcategory_id)
                                  .where(Items.count > 0))
        item = result.scalars().first()
        await db.close()
        if item is None:
            await query.answer("В данной подкатегори нету товаров")

    if item:
        await state.update_data({"selected_item_id": item.id})
        description_text = f"Название: {item.name}\nЦена: {item.price}\nОписание: {item.description}"
        photo = types.InputMediaPhoto(media=types.FSInputFile(pathlib.Path(media_dir) / item.photo), caption=description_text)
        try:
            await query.message.edit_media(media=photo, reply_markup=menu_catalog)
        except TelegramBadRequest as exept:
            chat_id = query.message.chat.id
            await query.message.delete()
            await query.message.answer_photo(photo=types.FSInputFile(pathlib.Path(media_dir) / item.photo),
                                             caption=description_text, reply_markup=menu_catalog)



@catalog_router.callback_query(ItemCallback.filter(F.action_type == "add"), GetItem.select_item)
async def ask_item_count(query: types.CallbackQuery, callback_data: ItemCallback, state: FSMContext):
    log_info(f"User {query.from_user.id}| get count add")
    await query.message.delete()
    await query.message.answer("Введите колличество товара")
    await state.set_state(GetItem.get_count)


@catalog_router.message(GetItem.get_count, F.text.isdigit())
async def add_item(message: types.Message, state: FSMContext):
    log_info(f"User {message.from_user.id}| get accept add on basket")
    state_data = await state.get_data()
    await state.update_data({'item_count': int(message.text)})
    db = async_session()
    item_id = state_data.get('selected_item_id')
    result = await db.execute(select(Items).where(Items.id == item_id))
    await db.close()
    item = result.scalar_one_or_none()
    await state.set_state(GetItem.accept)
    await message.answer(f"Добавить в корзину?:\n"
                         f"Товар: {item.name}\n"
                         f"В колличестве: {int(message.text)} шт.", reply_markup=yes_no_keyboard)



@catalog_router.message(F.text.lower() == "да", GetItem.accept)
async def accept_add(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    item_id = state_data.get('selected_item_id')
    item_count = state_data.get('item_count')
    db = async_session()
    basket_id = state_data.get('basket_id')
    basket_item_id = state_data.get('basket_item_id')
    result = None
    log_info(f"User {message.from_user.id}| get item and count to add in basket, {basket_id=}, {basket_item_id=}, {item_id=}")
    if basket_id:
        result = await db.execute(select(BasketItems)
                                  .where(BasketItems.basket_id == basket_id)
                                  .where(BasketItems.item_id == item_id))

    elif basket_item_id:
        result = await db.execute(select(BasketItems)
                                  .where(BasketItems.id == basket_item_id))

    element = result.scalar_one_or_none()

    if element is None:

        basket_item = BasketItems(basket_id=basket_id, item_id=item_id, count=item_count)
        db.add(basket_item)
        log_info(
            f"User {message.from_user.id}| be create new basket_item {basket_item.id=}")
        await db.commit()
        await db.close()

    else:
        log_info(
            f"User {message.from_user.id}| add items in basket")
        element.count += item_count
        await db.commit()
        await db.close()


    await message.answer("Товар успешно добавлен", reply_markup=menu_keyboard.as_markup())
    await basket_main(message, state)


@catalog_router.message(F.text.lower() == "нет", GetItem.accept)
async def accept_add(message: types.Message, state: FSMContext):
    log_info(f"User {message.from_user.id}| deny add item in basket")
    await state.clear()
    await catalog_main(message, state)