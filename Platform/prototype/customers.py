import json
from urllib.parse import parse_qs

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from message.models import UserMessage
from project.models import Collection
from prototype.models import ProjectPrototype, Prototype
from team.models import Membership
from user.models import User


connect_list = {}




class PrototypeConsumer(WebsocketConsumer):

    def connect(self):
        # 将原型与用户连接，判断用户是否属于原型所属项目所属的team
        query_string = self.scope['query_string']
        query_params = parse_qs(query_string)
        prototypeId = query_params.get(b'prototypeId', [b''])[0].decode().split()[0]
        userId = query_params.get(b'userId', [b''])[0].decode().split()[0]
        user = User.objects.get(id=userId)
        prototype = Prototype(id=prototypeId)
        project_prototype = ProjectPrototype.objects.get(id=prototypeId)
        project = project_prototype.project
        project_collection = Collection.objects.get(project=project)
        team = project_collection.team
        try:
            membership = Membership.objects.get(user=user, team=team)
        except:
            return

        if prototypeId not in connect_list:
            connect_list[prototypeId] = []
        if self not in connect_list[prototypeId]:
            connect_list[prototypeId].append(self)
        self.room_group_name = "prototype"
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

        componentData = prototype.componentData
        canvasStyleData = prototype.canvasStyleData

        self.send(json.dumps(componentData))
        self.send(json.dumps(canvasStyleData))

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def websocket_receive(self, message):
        message = message['message']
        userId = message['userId']

        # self.send(json.dumps())


