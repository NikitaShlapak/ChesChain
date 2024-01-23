import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chat.models import BoardRoom


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print('connect')
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print('receive:',text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        print('chat_message')
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))


class BoardConsumer(WebsocketConsumer):
    def connect(self):
        print('connect')
        self.board_name = self.scope["url_route"]["kwargs"]
        print(self.board_name)
        self.boardRoom = BoardRoom.objects.get(name=self.board_name['room_name'])
        #print(self.board.main_position)
        self.board_group_name = "board"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.board_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.board_group_name, self.channel_name
        )


    # Receive message from WebSocket
    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        position = text_data_json["position"]
        print('receive', text_data)
        # Send message to room group

        #board_room=BoardRoom.objects.get(name=self.board_name['room_name'])
        self.boardRoom.main_position=position
        self.boardRoom.save()
        async_to_sync(self.channel_layer.group_send)(
            self.board_group_name, {"type": "move", "position": position}
        )

    # Receive message from room group
    def move(self, event):
        position = event["position"]
        print('chat_message', position)
        # Send message to WebSocket
        self.send(text_data=json.dumps({"position": position}))