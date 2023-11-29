import os
import logging
from datetime import datetime

from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


load_dotenv(".env.dev.telegram")

try:
    logging.basicConfig(level=logging.INFO,
                        filename=f'loggs/devlog{datetime.now().strftime("%d-%m-%Y")}.log',filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
except FileNotFoundError:
    os.makedirs("loggs/")
    logging.basicConfig(level=logging.INFO,
                        filename=f'loggs/devlog{datetime.now().strftime("%d-%m-%Y")}.log', filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")


DB_ENGINE = os.environ.get('DB_ENGINE')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')

media_dir = os.environ.get('MEDIA_FILES')
site_host = os.environ.get('SITE_HOST')

engine = create_async_engine(f"{DB_ENGINE}+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
async_session = async_sessionmaker(engine)

bot = Bot(token=os.environ.get('TELEGRAM_TOKEN'))
dispatcher = Dispatcher()

