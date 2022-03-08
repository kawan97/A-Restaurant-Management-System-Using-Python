from channels.generic.websocket import WebsocketConsumer
import json
from random import randint
from time import sleep
class dataConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        for i in range(100):
            self.send(json.dumps({'value':randint(1,1000)}))
            sleep(1)
