from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 有客户端向后端改善websocket请求时自动触发
        # 服务端允许执行下行代码，如果不允许可以用 raise StopConsummer()拒绝客户端的连接请求
        self.accept()

    def websocket_receive(self, message):
        # 客户端发来数据时触发，message是客户端发来的数据（一个字典）
        print(message)
        self.send("服务器端的内容")  # 向客户端发送数据

    def websocket_disconnect(self, message):
        # 断开连接时触发
        raise StopConsumer()
