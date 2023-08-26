from django.shortcuts import render

# Create your views here.


from django.shortcuts import render

from channels.generic.websocket import WebsocketConsumer  # 基类


class ChatConsumer(WebsocketConsumer):
    """
    这里需要重载WebsocketConsumer父类的必要执行方法
    """
    # 客户端发起连接时
    def connect(self):  # self为每个客户端WebsocketConsumer对象的连接状态
        print('收到客户端websocket连接请求')
        self.accept()  # 服务端检验客户端合法性并保持，否则连接后直接断开
        # 给客户端发送消息
        self.send('您已连接成功')

    # 当客户端向服务端发送数据时
    def receive(self, text_data=None, bytes_data=None):
        print(f'来自{self}的消息{text_data}')  # 收到客户端的消息
        self.send('hello client')

    # 当客户端（非服务端）主动断开连接时：客户端ws.close()
    def disconnect(self, code):
        print(f'客户端{self}断开连接')