import json
from urllib.parse import parse_qs

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from message.models import UserMessage
from user.models import User



def getMessage(userId, read): # read:1 已读消息， read: 0 未读消息
    user = User.objects.get(id=userId)
    userMessages = UserMessage.objects.filter(user=user)
    unread = []
    for userMessage in userMessages:
        message = userMessage.message
        if message.status == read:
            unread.append({
                'time': str(message.time.strftime("%Y-%m-%d %H:%M:%S")),
                'content': message.content,
                'link': message.link,
                'messageId': message.id,
                'isInvited': message.isInvited
            })
    return unread


class MessageConsumer(WebsocketConsumer):

    def connect(self):
        query_string = self.scope['query_string']
        query_params = parse_qs(query_string)
        userId = query_params.get(b'userId', [b''])[0].decode().split()[0]

        # user = User.objects.get(id=userId)
        # userMessages = UserMessage.objects.filter(user=user)
        # unread = []
        # for userMessage in userMessages:
        #     message = userMessage.message
        #     if not message.status:
        #         unread.append({
        #             'time': str(message.time.strftime("%Y-%m-%d %H:%M:%S")),
        #             'content': message.content,
        #             'link': message.link,
        #             'messageId': message.id,
        #             'isInvited': message.isInvited
        #         })
        unread = getMessage(userId, 0)

        self.room_group_name = "user_message"
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

        self.send(json.dumps(unread))

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def send_update(self, event):
        message = event['message']
        userId = event['userId']
        unread = getMessage(userId, 0)

        self.send(json.dumps(unread))


