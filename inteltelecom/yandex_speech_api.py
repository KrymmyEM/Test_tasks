import requests
from pathlib import Path
from typing import Union
import enum

class TokenTypes(enum.Enum):
    API = "api"
    IAM = "iam"


class YandexSpeechApi:
    """
    Это достаточно старый код, потому и первая версия.
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

    def recognize(self, audioFile: Union[str, Path]):

        URL = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?"
        with open(f"{audioFile}", "rb") as f:
            data = f.read()

        headers = self.headers

        params = "&".join([
            "topic=general",
            "folderId=%s" % self.folder_id,
            "lang=ru-RU",
            "format=lpcm",
            "sampleRateHertz=48000"
        ])

        url = request.Request(URL + "%s" % params, data=data, headers=headers)
        responseData = request.urlopen(url).read().decode('UTF-8')
        result = json.loads(responseData)

        return result["result"]

    def synthesize(self, text: str, output: Union[str, Path] = "output"):

        URL = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'

        headers = self.headers

        data = parse.urlencode({
            'text': text,
            'lang': 'ru-RU',
            'folderId': self.folder_id,
            'format': 'lpcm',
            'sampleRateHertz': 48000,
        }).encode()

        req = request.Request(URL, data, headers)
        resp = request.urlopen(req)

        with open(output, "wb") as f:
            for audio_content in resp:
                f.write(audio_content)

        return True