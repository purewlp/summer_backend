import base64
import datetime
import json
import sys
from urllib.parse import parse_qs
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from django.core.files.base import ContentFile

from chat.models import UserRoom, Room, ChatMessage
from user.models import User

connect_list = {}  # 一个元素对应一个房间


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 校验连接
        query_string = self.scope['query_string']
        query_params = parse_qs(query_string)
        roomId = query_params.get(b'roomId', [b''])[0].decode().split()[0]
        userId = query_params.get(b'userId', [b''])[0].decode().split()[0]
        if userId is not None:
            if UserRoom.objects.filter(user__id=userId, room__id=roomId):
                print(userId)
                if roomId not in connect_list:
                    connect_list[roomId] = []
                if self not in connect_list[roomId]:
                    connect_list[roomId].append(self)
                self.connect()
                return
        self.close()

    def websocket_receive(self, message):
        # 接收消息
        query_string = self.scope['query_string']
        query_params = parse_qs(query_string)
        roomId = query_params[b'roomId'][0].decode().split()[0]
        userId = query_params[b'userId'][0].decode().split()[0]
        if (userId is None) or (not User.objects.filter(id=userId)) or (not Room.objects.filter(id=roomId)):
            self.send("error: cannot find user or room!")
            return
        user = User.objects.get(id=userId)
        try:
            dic = json.loads(message['text'])
        except json.JSONDecodeError as e:
            self.send("格式错误")
            return
        # 图片
        if 'image' in dic:
            image_base64 =str(dic['image']).split(",")[1]
            image_data = base64.b64decode(image_base64)
            chatMessage = ChatMessage.objects.create(
                isImage=True,
                auther=User.objects.get(id=userId),
                room=Room.objects.get(id=roomId)
            )
            chatMessage.image.save(name=f"{roomId}_{userId}.jpg", content=ContentFile(image_data), save=True)
            for connect in connect_list[roomId]:
                ret_dit = {
                    "id": str(chatMessage.id),
                    'authorId': str(userId),
                    'type': 'image',
                    'authorName': str(user.nickname),
                    'avatar': 'http://43.143.140.26/'+'media/' + str(user.avatar),
                    'time': str(chatMessage.sentTime.strftime("%Y-%m-%d %H:%M:%S")),
                    'image': 'http://43.143.140.26/'+'media/' + str(chatMessage.image),
                    'content': '',
                    'file': '',
                    'fileName': str(chatMessage.image).split("/")[len(str(chatMessage.image).split("/")) - 1]
                }
                connect.send(json.dumps(ret_dit))
        # 文件
        elif 'file' in dic:
            file_base64 =str(dic['file']).split(",")[1]
            file_data = base64.b64decode(file_base64)
            fileName = str(dic['fileName'])
            chatMessage = ChatMessage.objects.create(
                isImage=False,
                auther=User.objects.get(id=userId),
                room=Room.objects.get(id=roomId)
            )
            chatMessage.file.save(name=f"{fileName}", content=ContentFile(file_data), save=True)
            for connect in connect_list[roomId]:
                ret_dit = {
                    "id": str(chatMessage.id),
                    'authorId': str(userId),
                    'type': 'file',
                    'authorName': str(user.nickname),
                    'avatar': 'http://43.143.140.26/'+'media/' + str(user.avatar),
                    'time': str(chatMessage.sentTime.strftime("%Y-%m-%d %H:%M:%S")),
                    'image': '',
                    'content': '',
                    'file': 'http://43.143.140.26/'+'media/' + str(chatMessage.file),
                    'fileName': str(chatMessage.file).split("/")[len(str(chatMessage.file).split("/")) - 1]
                }
                connect.send(json.dumps(ret_dit))
        # 文字
        elif 'text' in dic:
            text = str(dic['text'])
            chatMessage = ChatMessage.objects.create(
                isImage=False,
                content=text,
                auther=user,
                room=Room.objects.get(id=roomId)
            )
            for connect in connect_list[roomId]:
                ret_dit = {
                    "id": str(chatMessage.id),
                    'authorId': str(userId),
                    'type': 'text',
                    'authorName': str(user.nickname),
                    'avatar': 'http://43.143.140.26/'+'media/' + str(user.avatar),
                    'time': str(chatMessage.sentTime.strftime("%Y-%m-%d %H:%M:%S")),
                    'image': '',
                    'content': text,
                    'file': '',
                    'fileName': ''
                }
                connect.send(json.dumps(ret_dit))
        elif 'emoji' in dic:
            text = str(dic['emoji'])
            chatMessage = ChatMessage.objects.create(
                isImage=False,
                isEmoji=True,
                content=text,
                auther=user,
                room=Room.objects.get(id=roomId)
            )
            for connect in connect_list[roomId]:
                ret_dit = {
                    "id": str(chatMessage.id),
                    'authorId': str(userId),
                    'type': 'emoji',
                    'authorName': str(user.nickname),
                    'avatar': 'http://43.143.140.26/'+'media/' + str(user.avatar),
                    'time': str(chatMessage.sentTime.strftime("%Y-%m-%d %H:%M:%S")),
                    'image': '',
                    'content': text,
                    'file': '',
                    'fileName': ''
                }
                connect.send(json.dumps(ret_dit))

    def websocket_disconnect(self, message):
        # 断开连接
        for connect in connect_list:
            if str(self) in connect:
                connect.remove(self)
                break
        raise StopConsumer()


# Create your views here.


# from django.shortcuts import render
#
# from channels.generic.websocket import WebsocketConsumer  # 基类
#
#
# class ChatConsumer(WebsocketConsumer):
#     """
#     这里需要重载WebsocketConsumer父类的必要执行方法
#     """
#     # 客户端发起连接时
#     def connect(self):  # self为每个客户端WebsocketConsumer对象的连接状态
#         print('收到客户端websocket连接请求')
#         self.accept()  # 服务端检验客户端合法性并保持，否则连接后直接断开
#         # 给客户端发送消息
#         self.send('您已连接成功')
#
#     # 当客户端向服务端发送数据时
#     def receive(self, text_data=None, bytes_data=None):
#         print(f'来自{self}的消息{text_data}')  # 收到客户端的消息
#         self.send('hello client')
#
#     # 当客户端（非服务端）主动断开连接时：客户端ws.close()
#     def disconnect(self, code):
#         print(f'客户端{self}断开连接')
