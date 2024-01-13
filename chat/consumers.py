from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
import json
from .models import Group, Chat
from channels.db import database_sync_to_async

class chatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]  # room_name = indian

        await self.channel_layer.group_add(self.room_name, self.channel_name)

        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        text_data_json = json.loads(event['text'])
        message = text_data_json["message"]

        group = await database_sync_to_async(Group.objects.get)(name = self.room_name)
        chat = await database_sync_to_async(Chat)(content = message, group = group)
        await database_sync_to_async(chat.save)()

        user = self.scope["user"]
        if user.is_authenticated:
            username = str(user.username)
        else: 
            username = "uknown"

        complete_msg = {"user": username, "message": message}

        await self.channel_layer.group_send(
            self.room_name, {
                "type": "chat_message",
                "message": json.dumps(complete_msg)
            }
        )


    async def chat_message(self, event):
        message_dict = json.loads(event["message"])
        await self.send({
            "type": "websocket.send",
            "text": json.dumps(message_dict)
        })
        
            
    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        raise StopConsumer()

