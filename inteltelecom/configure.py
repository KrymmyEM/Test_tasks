import os
import pathlib
from dotenv import load_dotenv

BASE_DIR = pathlib.Path(__file__).resolve(strict=True).parent


DEBUG = load_dotenv(".env")


ASTERISK_ARI_URL=getenv("ASTERISK_ARI_URL")
ASTERISK_ARI_LOGIN=getenv("ASTERISK_ARI_LOGIN")
ASTERISK_ARI_PASSWORD=getenv("ASTERISK_ARI_PASSWORD")
ASTERISK_APP_NAME=getenv("ASTERISK_APP_NAME")
ASTERISK_CALL_ENDPOINT=getenv("ASTERISK_CALL_ENDPOINT")

PLAYBACK_STORAGE: str = getenv("PLAYBACK_STORAGE")

if PLAYBACK_STORAGE.startswith("/"):
    PLAYBACK_STORAGE = pathlib.Path(PLAYBACK_STORAGE)
else:
    PLAYBACK_STORAGE = BASE_DIR / PLAYBACK_STORAGE


TEXT_STORAGE: str = getenv("TEXT_STORAGE")

if TEXT_STORAGE.startswith("/"):
    TEXT_STORAGE = pathlib.Path(TEXT_STORAGE)
else:
    TEXT_STORAGE = BASE_DIR / TEXT_STORAGE


RECORD_STORAGE: pathlib.Path = pathlib.Path(getenv("RECORD_STORAGE"))


YANDEX_TOKEN=getenv("YANDEX_TOKEN")
YANDEX_FOLDERID=getenv("YANDEX_FOLDERID")

TOKEN_TYPE = getenv("TOKEN_TYPE")
