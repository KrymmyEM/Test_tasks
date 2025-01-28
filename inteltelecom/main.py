
import asyncio
import json
import os
import pathlib

import websockets

import configure
from send_models import *
from models import *
from asterisk import ARI_Client
from yandex_speech_api import YandexSpeechApi, TokenTypes


CHANNEL_ACTIONS=['StasisStart', 'PlaybackStarted', 'PlaybackFinished', 'RecordingStarted', 'RecordingFinished', 'StasisEnd']

async def main():
    algoritm = {
        [
            {
                "mode":"playback", 
                "data": {
                    "filename": "first.opus",
                    "text": "Привет, проврека как работает бот"
                }
            }, 
            {
                "mode": "record", 
                "data": {
                "record_data": RecordingConfig(
                    name="test",
                    format="wav",
                    maxDurationSeconds=0,
                    maxSilenceSeconds=1,
                    ifExists="overwrite"
                ),
                "textfile": "test.txt"
            }
            },
            {
                "mode":"playback", 
                "data": {
                    "filename": "second.opus",
                    "text": "Спасибо за информацию"
                }
            },
        ]
    }
    call_to = input("Call to:")
    client = ARI_Client(configure.ASTERISK_ARI_URL, configure.ASTERISK_ARI_LOGIN, configure.ASTERISK_ARI_PASSWORD, configure.ASTERISK_APP_NAME)
    yandex_speech_api = YandexSpeechApi(configure.YANDEX_TOKEN, configure.YANDEX_FOLDERID, TokenTypes[configure.TOKEN_TYPE])
    channel = None
    step = 0
    async with client as websocket:
        channel = await client.channels(CallConfig(
            endpoint=configure.ASTERISK_CALL_ENDPOINT,
            extension=call_to
        ))
        for message in websocket:
            message = json.loads(message)
            message_type = message.get("type")
            if message_type != CHANNEL_ACTIONS:
                continue

            step_data = algoritm[step]
            mode = step_data.get("mode")
            data = step_data.get("data")
            
            if message_type == "StasisStart":
                if not channel:
                    channel = Channel(message.get("channel"))
            
            elif message_type == "PlaybackFinished":
                step += 1
            elif message_type == "RecordingFinished":
                record_data: RecordingConfig = data.get("record_data")
                audio_file: pathlib.Path = configure.RECORD_STORAGE / record_data.name + "." + record_data.format
                text_file = data.get("textfile")
                yandex_speech_api.recognize(audio_file, configure.TEXT_STORAGE / text_file)
                step += 1

            
            if mode == "playback":
                file_path: pathlib.Path = configure.PLAYBACK_STORAGE / data.get("filename")
                create_file = file_path.is_file()
                if create_file:
                    if not yandex_speech_api.synthesize(data.get("text"), file_path):
                        break
                client.channels(MediaPlaybackConfig(
                        "sound:"+str(file_path)
                    ),
                    {"channelId": channel.id}
                )
            elif mode == "record":
                record_data = data.get("record_data")
                client.channels(
                    record_data,
                    {"channelId": channel.id}
                )