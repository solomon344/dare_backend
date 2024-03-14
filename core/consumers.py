from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from .models import User,Message,Room
import json

async def Create_Message(message,user_id,group_id):
    user = await User.objects.get(pk=id)
    group = await Room.objects.get(pk=id)
    if user is not None and group is not None:
        msg  = await Message(message=message,by=user,room=group)
        msg.save()

class roomConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"play_{self.room_name}"
        self.accept()

        #join a group or room
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
    
    def disconnect(self, code):

        #leave group or room
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        

    def receive(self, text_data=None, bytes_data=None):

        # retrieve message from websocket javascrip
        text_data_string = json.loads(text_data)
        message = text_data_string['message']
        from_id = text_data_string['from_id']
        to_id = text_data_string['to_id']
        group_id = text_data_string['group_id']
        msg_type = text_data_string['msg_type']
        print(message)
        #send message to the room or group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message,"from_id":from_id,'to_id':to_id,"group_id":group_id,'msg_type':msg_type}
        )
        
    def chat_message(self, event):
        #recieve message from room or group
        message = event["message"]
        from_id = event['from_id']
        to_id = event['to_id']
        group_id = event['group_id']
        msg_type = event['msg_type']
        print(message)
        # Create_Message(message,user_id,group_id)

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message,"from_id":from_id,'to_id':to_id,"group_id":group_id,'msg_type':msg_type}))