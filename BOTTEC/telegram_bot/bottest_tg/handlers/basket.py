import datetime
import pathlib

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot_elements.callback import ItemCallback, PaymentCallBack
from bot_elements.keyboards import keyboard_inline_builder, menu_basket_item, menu_catalog, yes_no_keyboard, \
    menu_keyboard, menu_basket
from bot_elements.states import GetItem, MakeOrder
from handlers import checkers
from handlers import cataloge
from init_base import bot, async_session, media_dir, site_host
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router, F, types
from sqlalchemy import select

from models.base_models import Users, Baskets, Items, BasketItems, AddressesDeliver, Orders, PaymentService
from services.mini_services import generate_random_string, log_info

basket_router = Router(name="basket")

@basket_router.message(F.text.lower() == "корзина")
@checkers.control_user
async def basket_main(message: types.Message, state: FSMContext, **kwargs):
    await state.set_state(GetItem.select_item_on_basket)
    log_info(f"User {message.from_user.id}| watch basket")
    await message.answer(text="Ваша корзина:", reply_markup=menu_basket)
    async with async_session() as db:
        result = await db.execute(select(BasketItems)
                                  .join(Users, Users.tg_id == message.from_user.id)
                                  .join(Baskets, Baskets.user_id == Users.id).where(Baskets.sell == False))

    basket_items = result.scalars()
    count_item = 0
    local_builder = keyboard_inline_builder()
    for basket_item in basket_items:

        result = await db.execute(select(Items).where(Items.id == basket_item.item_id))
        item = result.scalar_one_or_none()
        if item is None:
            continue
        if count_item == 0:
            await state.set_data({"basket_id": basket_item.basket_id})
        count_item += 1
        local_builder.button(text=f"{item.name}|{basket_item.count} шт.",
                             callback_data=ItemCallback(action_type="show",
                                                        item_id=basket_item.item_id,
                                                        basket_item_id=basket_item.id).pack())

    if count_item:
        local_builder.adjust(1)
        await message.answer('Список товаров', reply_markup=local_builder.as_markup())

    else:
        log_info(f"User {message.from_user.id}| basket empty go to cataloge")
        await message.answer('В корзине нету товаров, вы их можете посмотреть в нашем каталоге')
        await cataloge.catalog_main(message, state)

    await db.close()




@basket_router.callback_query(ItemCallback.filter(F.action_type == "show"), GetItem.select_item_on_basket)
async def show_item(query: types.CallbackQuery, callback_data:  ItemCallback, state: FSMContext):
    db = async_session()
    data_callback_type = type(callback_data)

    state_data = await state.get_data()
    selected_item_id = callback_data.item_id
    basket_item_id = callback_data.basket_item_id
    log_info(f"User {query.from_user.id}| watch on item {selected_item_id=}")
    result = await db.execute(select(Items).where(Items.id == selected_item_id))

    item = result.scalar_one_or_none()
    await db.close()
    if item:
        await state.update_data({"selected_item_id": item.id, 'basket_item_id': basket_item_id})
        description_text = f"Название: {item.name}\nЦена: {item.price}\nОписание: {item.description}"
        photo = types.InputMediaPhoto(media=types.FSInputFile(pathlib.Path(media_dir) / item.photo), caption=description_text)
        try:
            await query.message.edit_media(media=photo, reply_markup=menu_basket_item)
        except TelegramBadRequest as exept:
            chat_id = query.message.chat.id
            await query.message.delete()
            await query.message.answer_photo(photo=types.FSInputFile(pathlib.Path(media_dir) / item.photo),
                                             caption=description_text, reply_markup=menu_basket_item)


@basket_router.callback_query(ItemCallback.filter(F.action_type == "del"), GetItem.select_item_on_basket)
async def ask_item_count(query: types.CallbackQuery, callback_data: ItemCallback, state: FSMContext):
    await state.set_state(GetItem.del_item)
    await query.message.delete()
    log_info(f"User {query.from_user.id}| delete items")
    log_info(f"User {query.from_user.id}| add items")
    keyboard = ReplyKeyboardBuilder().add(KeyboardButton(text="Удалить все"))
    await query.message.answer("Введите колличество товара",
                               reply_markup=keyboard.as_markup())



@basket_router.message(GetItem.del_item, F.text.isdigit())
@basket_router.message(GetItem.del_item, F.text.lower() == 'удалить все')
async def add_item(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    log_info(f"User {message.from_user.id}| get count delete items")
    db = async_session()
    item_id = state_data.get('selected_item_id')
    basket_item_id = state_data.get('basket_item_id')
    result = await db.execute(select(Items).where(Items.id == item_id))
    item = result.scalar_one_or_none()
    result = await db.execute(select(BasketItems).where(BasketItems.id == basket_item_id))
    basket_item = result.scalar_one_or_none()
    await db.close()
    count_item = -1 if message.text.lower() == 'удалить все' else int(message.text)
    if count_item == -1 or basket_item.count - count_item <= 0:
        await message.answer(f"Удалить корзины полностью?:\n"
                             f"Товар: {item.name}\n", reply_markup=yes_no_keyboard)
        await state.update_data({'del_item_count': -1})
    else:
        await message.answer(f"Удалить корзины {count_item} шт.?:\n"
                             f"Товара: {item.name}\n", reply_markup=yes_no_keyboard)
        await state.update_data({'del_item_count': count_item})

    await state.set_state(GetItem.del_accept)


@basket_router.message(F.text.lower() == "да", GetItem.del_accept)
async def accept_add(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    log_info(f"User {message.from_user.id}| accept delete item in basket")
    basket_item_id = state_data.get('basket_item_id')
    del_count = state_data.get('del_item_count')
    db = async_session()
    result = await db.execute(select(BasketItems)
                              .where(BasketItems.id == basket_item_id))

    basket_item = result.scalar_one_or_none()
    if del_count == -1:
        await db.delete(basket_item)

    else:
        basket_item.count -= del_count

    await db.commit()
    await db.close()
    await message.answer("Товар успешно удален", reply_markup=menu_keyboard.as_markup())
    await basket_main(message, state)


@basket_router.message(F.text.lower() == "нет", GetItem.del_accept)
async def accept_add(message: types.Message, state: FSMContext):
    log_info(f"User {message.from_user.id}| deny delete ")
    await state.clear()
    await basket_main(message, state)


@basket_router.message(GetItem.select_item_on_basket, F.text.lower() == "оформить заказ")
@basket_router.message(MakeOrder.check_address, F.text.lower() == "нет")
async def ask_address(message: types.Message, state: FSMContext):
    log_info(f"User {message.from_user.id}| get address deliver")
    await state.set_state(MakeOrder.get_address)
    # async with async_session() as db:
    #     result = await db.execute(select(AddressesDeliver)
    #                      .join(Users, Users.tg_id == message.from_user.id)
    #                      .where(AddressesDeliver.user_id == Users.id))
    #
    #     addresses_deliver = result.scalars()
    #
    # local_reply_keyboard = ReplyKeyboardBuilder()
    # for address in addresses_deliver:
    #     local_reply_keyboard.button(text=address.adress)

    await message.answer("Введите адрес доставки")

@basket_router.message(MakeOrder.get_address)
async def ask_address_deliver(message: types.Message, state: FSMContext):
    log_info(f"User {message.from_user.id}| accept address deliver")
    await state.set_state(MakeOrder.check_address)
    await state.update_data({'address_deliver': message.text})
    await message.answer(f"Доставить заказ по: {message.text}\nВсе верно?", reply_markup=yes_no_keyboard)


@basket_router.message(MakeOrder.check_address, F.text.lower() == "да")
async def ask_payment_service(message: types.Message, state: FSMContext):
    log_info(f"User {message.from_user.id}| get payment service")
    await state.set_state(MakeOrder.set_payment_service)
    state_data = await state.get_data()
    order_id = await generate_random_string(10)
    address_deliver = state_data.get('address_deliver')
    basket_id = state_data.get('basket_id')
    price = 0.0
    async with async_session() as db:
        result = await db.execute(select(BasketItems)
                                  .where(BasketItems.basket_id == basket_id))

        for basket_item in result.scalars():
            result_items = await db.execute(select(Items)
                                      .where(Items.id == basket_item.item_id))
            item: Items = result_items.scalar_one_or_none()

            price += float(item.price) * basket_item.count

        db.add(Orders(order_id=order_id, address_deliver=address_deliver,
                      price=price, basket_id=basket_id, created_at=datetime.datetime.now()))
        await db.commit()

    local_keyboard = keyboard_inline_builder()
    async with async_session() as db:
        result = await db.execute(select(PaymentService))
        for payment_service in result.scalars():
            local_keyboard.button(text=payment_service.name.capitalize(),
                                  callback_data=PaymentCallBack(status='red',
                                                                payment_service=payment_service.id,
                                                                order_id=order_id))

    await message.answer("Выберите способ оплаты", reply_markup=local_keyboard.as_markup())


@basket_router.callback_query(PaymentCallBack.filter(F.status == 'red'))
async def ask_item_count(query: types.CallbackQuery, callback_data: PaymentCallBack, state: FSMContext):
    async with async_session() as db:
        log_info(f"User {query.from_user.id}| get link on redirect")
        result = await db.execute(select(Orders).where(Orders.order_id == callback_data.order_id))
        order: Orders = result.scalar_one_or_none()
        order.payment_id = callback_data.payment_service
        order.payment_status_id = 1
        await db.commit()

    await query.message.edit_text("Последнее действие", reply_markup=keyboard_inline_builder()
                                  .button(text="Оплата", url=f"{site_host}/orders/{callback_data.order_id}/redirect")
                                  .as_markup())
    await query.message.answer(text="Мы свяжемся с вами при необходимости", reply_markup=menu_keyboard.as_markup())
