
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from init_base import dispatcher, bot, async_session

from aiogram import F, Router
from aiogram import filters, types

from handlers import checkers
from bot_elements.keyboards import menu_keyboard

menu_router = Router(name="menu")


@menu_router.message(filters.CommandStart())
@menu_router.message(F.text.lowercase() == "меню")
@checkers.control_user
async def menu(message: types.Message, state: FSMContext, **kwargs):
    await message.answer("Добро пожаловать наш телеграмм бот!", reply_markup=menu_keyboard.as_markup())


@menu_router.message(filters.Command("cancel"))
@menu_router.message(F.text.casefold() == "cancel" or F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=menu_keyboard.as_markup(),
    )