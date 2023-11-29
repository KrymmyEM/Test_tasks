from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot_elements.callback import QuestionsCallBack
from bot_elements.keyboards import keyboard_inline_builder
from init_base import bot, async_session
from models.base_models import Questions
from sqlalchemy import select
from aiogram import Router, F, types


faq_router = Router(name="faq")


@faq_router.message(F.text.lower() == "faq")
async def faq_main(message: types.Message, state: FSMContext):
    local_keyboard = keyboard_inline_builder()
    async with async_session() as db:
        result = await db.execute(select(Questions).order_by(Questions.count.desc()))
        first_ten = result.scalars().fetchmany(10)
        for quest in first_ten:
            local_keyboard.button(text=quest.question, callback_data=QuestionsCallBack(act='show', quest_id=quest.id))

    local_keyboard.adjust(1)
    await message.answer("Популярные вопросы:",
                         reply_markup=local_keyboard.as_markup())


@faq_router.callback_query(QuestionsCallBack.filter(F.act == "show"))
async def ask_item_count(query: types.CallbackQuery, callback_data: QuestionsCallBack):
    async with async_session() as db:
        result = await db.execute(select(Questions).where(Questions.id == callback_data.quest_id))
        question: Questions = result.scalar_one_or_none()
        answer = question.answer if question.answer or question.answer == '' else "__На данный момент ответа на вопрос нету__"
        await query.message.answer(text=f"Вопрос:{question.question}\nОтвет:{question.answer}")
        question.count += 1
        await db.commit()

