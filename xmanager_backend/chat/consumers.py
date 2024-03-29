from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message, Chat, Profile

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        messages = Chat.last_10_messages(data['chatId'])
        if (messages):
            content = {
            'command' : 'messages',
            'messages' : self.messages_to_json(messages)
            }
        else:
            content = {
                'command': 'messages',
                'messages': 'No message yet'
            }
        self.send_message(content)


    def new_message(self, data):
        user_contact = get_object_or_404(User, username=data['from'])
        message = Message.objects.create(
            author = user_contact, 
            content = data['message'])
        current_chat = Chat.get_current_chat(data['chatId'])
        current_chat.messages.add(message)
        current_chat.save()
        content = {
            'command' : 'new_message',
            'message' : self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result= [] 
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages' : fetch_messages,
        'new_message' : new_message
    }

    
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        #message = data['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )


    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        async_to_sync(self.send(text_data=json.dumps(message)))