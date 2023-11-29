import logging
import asyncio
from sqlalchemy import select

from init_base import dispatcher, bot, engine, async_session
from models.base_models import Base, PaymentService, PaymentStatus
from handlers.menu import menu_router
from handlers.cataloge import catalog_router
from handlers.basket import basket_router
from handlers.faq import faq_router

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        result = await db.execute(select(PaymentService))
        payment_service = result.scalars().first()
        result = await db.execute(select(PaymentStatus))
        payment_status = result.scalars().first()

        if payment_service is None:
            db.add_all([PaymentService(name="yokassa"), PaymentService(name="tinkoff")])

        if payment_status is None:
            db.add_all([PaymentStatus(name="wait"), PaymentStatus(name="paid"), PaymentStatus(name="reject")])

        await db.commit()

    dispatcher.include_router(menu_router)
    dispatcher.include_router(catalog_router)
    dispatcher.include_router(basket_router)
    dispatcher.include_router(faq_router)
    print("Телеграмм бот запущен")
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


