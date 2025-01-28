import asyncio
import aiohttp
import websockets
import json
import urllib
from typing import Union

from send_models import *
from models import *

class Asterisk():

    def __init__(self, url: str, login: str, password: str, app: str):
        self.url = url
        self.login = login
        self.password = password
        self.token = self.login + ":" + self.password
        self.app = app

        self.headers = {
            "Authorization": "Basic " + token
        }
        self.messages = []
        self.session = aiohttp.ClientSession(headers=self.headers)
        self.websocket = websockets.connect(self.url+f"/events?app={self.app}&api_key={self.token}")

    async def _post(self, url, data):
        async with self.session as session:
            async with session.post(url, json=data) as response:
                return await response.json()
    
    async def _get(self, url, data: dict = {}):
        async with self.session as session:
            async with session.get(url, params=data) as response:
                if response.status != 200:
                    raise Exception("Status code: " + str(response.status))
                return await response.json()


    async def channels(self, parameters: Union[CallConfig, RecordingConfig, MediaPlaybackConfig, None] = None, **kwargs):
        url = self.url + "/channels"
        send_post: bool = parameters is not None
        channelId = kwargs.get("channelId", False)
        if channelId:
            url += f"/{channelId}"
        if send_post:
            use_model = Channel
            if parameters is CallConfig:
                parameters.app = self.app
                return Channel(await self._post(url, parameters.dict()))
            if parameters and channelId:
                paths = {
                    MediaPlaybackConfig: "play",
                    RecordingConfig: "record"
                }
                path = paths.get(type(parameters))
                url += "/"+path
                if path == "play":
                    playbackId = kwargs.get("playbackId", False)
                    if playbackId:
                        url += f"/{playbackId}"
                    use_model = Playback
                elif path == "record":
                    use_model = LiveRecording
            else:
                return None

            return use_model(await self._post(url, parameters.dict()))
        
        result = await self._get(url, {"api_key":self.token})
        if channelId:
            return Channel(result)
        return [Channel(channel) for channel in result]
    
    async def __aenter__(self):
        return self.websocket
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.websocket.close()
        