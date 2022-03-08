from channels.generic.websocket import AsyncWebsocketConsumer
import json
from random import randint
from asyncio import sleep
class dataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        for i in range(100):
            await self.send(json.dumps({'value':randint(1,1000)}))
            await sleep(1)