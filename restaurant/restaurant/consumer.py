from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from random import randint
from asyncio import sleep
class dataConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        group_name = 'myroom'
        self.group_name=group_name
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        print('IAM CONNECTEd')
        # for i in range(1):
        #     await self.send(json.dumps({'value':randint(1,1000)}))
        #     await sleep(1)
    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_message',
                'data': {
                    'data': data['value'],
                    'event': data['event'],
                    'username': data['username'],

                }
            }
        )

    async def send_message(self, event):
        await self.send(text_data=json.dumps(event['data']))