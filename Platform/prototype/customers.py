import json
from urllib.parse import parse_qs

from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer


from message.models import UserMessage
from project.models import Collection
from prototype.models import ProjectPrototype, Prototype
from team.models import Membership
from user.models import User


connect_list = {}




class PrototypeConsumer(WebsocketConsumer):

    def websocket_connect(self, message):
        # 将原型与用户连接，判断用户是否属于原型所属项目所属的team
        query_string = self.scope['query_string']
        query_params = parse_qs(query_string)
        prototypeId = query_params.get(b'prototypeId', [b''])[0].decode().split()[0]
        userId = query_params.get(b'userId', [b''])[0].decode().split()[0]
        user = User.objects.get(id=userId)
        prototype = Prototype.objects.get(id=prototypeId)
        project_prototype = ProjectPrototype.objects.get(prototype=prototype)
        project = project_prototype.project
        team = project.team
        try:
            membership = Membership.objects.get(user=user, team=team)
        except:
            return

        # print(self)

        if prototypeId not in connect_list:
            connect_list[prototypeId] = []
        if self not in connect_list[prototypeId]:
            connect_list[prototypeId].append(self)
        self.room_group_name = "prototype"
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()



        # componentData = prototype.componentData
        # canvasStyleData = prototype.canvasStyleData

        # prototypes = {
        #     "componentData": componentData,
        #     "canvasStyleData": canvasStyleData
        # }

        # self.send(json.dumps(prototypes))

    def websocket_disconnect(self, message):
        for connect in connect_list:
            if str(self) in connect:
                connect.remove(self)
                break
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
        self.disconnect(message['code'])
        raise StopConsumer()

    def websocket_receive(self, message):
        query_string = self.scope['query_string']
        query_params = parse_qs(query_string)
        prototypeId = query_params.get(b'prototypeId', [b''])[0].decode().split()[0]
        userId = query_params.get(b'userId', [b''])[0].decode().split()[0]

        # print(message)


        # dic = json.loads(message['text'])
        cid = message['text']
        cids = cid.split('$$$')
        componentData = cids[0]
        canvasStyleData = cids[1]
        # cid = json.loads(cid)

        print(componentData)
        print(canvasStyleData)



        prototype = Prototype.objects.get(id=prototypeId)
        prototype.componentData = componentData
        prototype.canvasStyleData = canvasStyleData
        prototype.save()

        for connect in connect_list[prototypeId]:
            prototypes = {
                "componentData": prototype.componentData,
                "canvasStyleData": prototype.canvasStyleData
            }

            if connect == self:
                continue
            connect.send(cid)


