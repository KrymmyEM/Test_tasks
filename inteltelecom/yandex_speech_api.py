import requests
from pathlib import Path
from typing import Union
import enum

class TokenTypes(enum.Enum):
    API = "api"
    IAM = "iam"


class YandexSpeechApi:
    """
    Есть старый код 4 летней давности
    """

    def __init__(self, token, folder_id, token_type: TokenTypes = TokenTypes.API):
        self.url = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"
        self.folder_id = folder_id
        authorization_text = ""
        if token_type == TokenTypes.IAM:
            authorization_text = "Authorization: Basic "
        elif token_type == TokenTypes.API:
            authorization_text = "Authorization: Api-Key "
        authorization_text = authorization_text + token
        self.headers = {
            "Authorization": authorization_text
        }
        self.session = aiohttp.ClientSession(headers=self.headers)

    def recognize(self, audioFile: Union[str, Path], output: Union[str, Path]):
        URL = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"

        # Открываем аудиофайл для чтения в бинарном режиме
        with open(audioFile, "rb") as f:
            data = f.read()

        # Формируем параметры запроса
        params = {
            "topic": "general",
            "folderId": self.folder_id,
            "lang": "ru-RU",
            "format": "lpcm",
            "sampleRateHertz": 48000
        }

        # Выполняем POST-запрос
        response = requests.post(URL, params=params, headers=self.headers, data=data)

        # Проверяем успешность запроса
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

        # Декодируем JSON-ответ
        result = response.json()

        # Записываем результат в выходной файл
        with open(output, "w") as file:
            file.write(result["result"])

        return True


    def synthesize(self, text: str, output: Union[str, Path] = "output", audio_format="oggopus"):

        URL = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'

        data = {
            'ssml'if ssml else 'text': text,
            'lang': 'ru-RU',
            'folderId': self.folder_id,
            'format': audio_format,
            'sampleRateHertz': 16000
        }

        response = requests.post(URL, data=data, headers=self.headers)

        if response.status_code != 200:
            return False

        if response.status_code == 200:
            with open(output, "wb") as f:
                for audio_content in response:
                    f.write(audio_content)

        return True