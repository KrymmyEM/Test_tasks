import asyncio

from bot_elements.keyboards import keyboard_inline_builder
from models.base_models import Users, CheckGroups, CheckChannels, Baskets
from init_base import bot, async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from aiogram import filters, types

from services.mini_services import log_info


async def check_user(user_id: int, db: AsyncSession = async_session()) -> dict[str, bool]:
    is_register: bool = False
    is_admin: bool = False
    follows_on_channels: bool = False
    follows_on_groups: bool = False
    result = await db.execute(select(Users).where(Users.tg_id == user_id))
    user_data: Users | None = result.scalar_one_or_none()
    u_d = str(user_data.__dict__)
    log_info(u_d)
    log_info(f"Check {user_id}|")
    if user_data:
        is_register = True
        is_admin = user_data.admin
        groups_empty = True
        channels_empty = True
        status_groups = []
        status_channels = []
        result_groups = await db.execute(select(CheckGroups))
        result_channels = await db.execute(select(CheckChannels))
        result_group_scal = result_groups.scalars()
        result_channel_scal = result_channels.scalars()
        try:
            for group, channel in result_group_scal, result_channel_scal:
                log_info(f"Check {user_id}| go to channel and group circle")
                log_info(f"Check {user_id}| {group.groups_id=}, {channel.channel_id=}")
                groups_empty = False
                channels_empty = False
                member_gr = await bot.get_chat_member(group.groups_id, user_id=user_id)
                member_ch = await bot.get_chat_member(channel.channel_id, user_id=user_id)
                status_groups.append(member_gr.status != "left")
                status_channels.append(member_ch.status != "left")

        except ValueError as err:
            log_info('Channels and groups not found')
            status_channels.append(True)
            status_groups.append(True)

        if groups_empty:
            status_groups.append(True)

        if channels_empty:
            status_channels.append(True)

        log_info(f"Check {user_id}|{status_groups=}, {status_channels=}")
        follows_on_groups = all(status_groups)
        follows_on_channels = all(status_channels)

    return {'is_register': is_register,
            'is_admin': is_admin,
            'follows_on_channels': follows_on_channels,
            'follows_on_groups': follows_on_groups}


def control_user(function):
    async def wrapper(input_user, *args, **kwargs):
        db: AsyncSession = async_session()
        user_id = input_user.from_user.id
        user_data = await check_user(user_id)
        is_register: bool = user_data.get('is_register')
        is_admin: bool = user_data.get('is_admin')
        follows_on_channels: bool = user_data.get('follows_on_channels')
        follows_on_groups: bool = user_data.get('follows_on_groups')
        log_info(f"Check user {user_id}| {user_data}")
        if not is_register:
            log_info(f"user {user_id}| registr")
            user = Users(tg_id=user_id, admin=False)
            db.add(user)
            await db.commit()
            await db.refresh(user)
            basket = Baskets(user_id=user.id, sell=False)
            db.add(basket)
            await db.commit()
            await db.close()

        if not follows_on_groups and not follows_on_channels:
            log_info(f"user {user_id}| not follows on channels or groups")
            channels_exist = False
            groups_exist = False
            local_keyboard_channels = keyboard_inline_builder()
            if not follows_on_channels:
                result = await db.execute(select(CheckChannels))
                for i, channel in enumerate(result.scalars()):
                    channels_exist = True
                    local_keyboard_channels.button(text=f'{i} канал', url=f"https://web.telegram.org/a/#{channel.channel_id}")
                local_keyboard_channels.adjust(3, 3)
            local_keyboard_groups = keyboard_inline_builder()
            if not follows_on_groups:
                result = await db.execute(select(CheckGroups))
                for i, group in enumerate(result.scalars()):
                    groups_exist = True
                    local_keyboard_groups.button(text=f'{i} группа', url=f"https://web.telegram.org/a/#{group.groups_id}")
                local_keyboard_groups.adjust(3, 3)


            if groups_exist or channels_exist:
                await input_user.answer("Для использования бота необходимо:")
                if channels_exist:
                    await input_user.answer('Подписатся на наши каналы телеграмм', reply_markup=local_keyboard_channels.as_markup())
                if groups_exist:
                    await input_user.answer('Подписатся на наши группы телеграмм', reply_markup=local_keyboard_groups.as_markup())
                return False

        if is_admin:
            return await function(input_user, *args, **kwargs)

        return await function(input_user, *args, **kwargs)

    return wrapper
