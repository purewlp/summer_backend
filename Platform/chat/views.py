import json
from django.core.files import File
from django.http import HttpResponse, HttpRequest, FileResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from user.models import User
from project.models import Project
from team.models import Team, Membership
from chat.models import Room, ChatMessage, UserRoom, Document


class RoomView(View):
    # 创建聊天室
    def post(self, request: HttpRequest):
        try:
            members = request.POST.get('members')
            teamId = request.POST.get('teamId')
            roomName = request.POST.get('roomName')
            userId = request.POST.get('userId')
        except:
            return HttpResponse({"status":400})


        try:
            user = User.objects.get(id=int(userId))
            team = Team.objects.get(id=int(teamId))
        except:
            return HttpResponse({"status":404})
        roomName = str(roomName)
        # 创建聊天室
        if not Room.objects.filter(team=team):
            room = Room.objects.create(team=team,name=roomName)
        else:
            return HttpResponse({"errno":"已存在房间"})
        members = list(members)
        for memberId in members:
            if User.objects.filter(id=int(memberId)):
                member = User.objects.get(id=int(memberId))
                if not UserRoom.objects.filter(room=room, user=member):
                    UserRoom.objects.create(room=room, user=member)
        if not UserRoom.objects.filter(room=room, user=user):
            UserRoom.objects.create(room=room, user=user)

        return HttpResponse({"status":200})


class MessageView(View):
    # 聊天室历史消息

    def get(self, request: HttpRequest):

        try:
            roomId = request.POST.get('roomId')
            userId = request.POST.get('userId')
        except:
            return HttpResponse(status=400)

        try:
            user = User.objects.get(id=int(userId))
            room = Room.objects.get(id=int(roomId))
        except:
            return HttpResponse(status=404)

        # 返回信息
        ans = {
            "messages": []
        }
        for message in ChatMessage.objects.filter(room=room):
            if message.isImage:
                image = 'chat/media/' + str(message.image)
                content = ''
                file = ''
                fileName = str(image).split("/")[len(str(image).split("/")) - 1]
                type = 'image'
            else:
                if message.content is not None:
                    content = message.content
                    image = ''
                    file = ''
                    fileName = ''
                    type = 'text'
                else:
                    content = ''
                    image = ''
                    file = 'chat/media/' + str(message.file)
                    fileName = str(file).split("/")[len(str(file).split("/")) - 1]
                    type = 'file'
            sub_ans = {
                "id": str(message.id),
                "authorId": str(message.auther.id),
                "type": str(type),
                "content": str(content),
                "authorName": str(message.auther.nickname),
                "avatar": 'chat/media/' + str(message.auther.avatar),
                "time": str(message.sentTime.strftime("%Y-%m-%d %H:%M:%S")),
                "image": str(image),
                "file": str(file),
                "fileName": str(fileName)
            }
            ans['messages'].append(sub_ans)
        return HttpResponse(json.dumps(ans), content_type='application/json', status=200)


class RoomList(View):
    # 获取聊天室列表

    def post(self, request: HttpRequest):

        userId = request.POST.get('userId')
        try:
            user = User.objects.get(id=userId)
        except:
            return HttpResponse(status=400)

        userRooms = UserRoom.objects.filter(user=user)
        for userRoom in userRooms:
            rooms = {
                'roomName': str(userRoom.room.name),
                'roomId': str(userRoom.room.id),
                'team': str(userRoom.room.team)
            }
        return HttpResponse(json.dumps(rooms), content_type='application/json', status=200)


class FileView(View):
    def post(self, request: HttpRequest):

        try:
            messageId = request.POST.get('roomId')
        except:
            return HttpResponse(status=400)
        message = ChatMessage.objects.get(id=messageId)
        if message.isImage:
            filePath = 'chat/media/' + str(message.image)
            try:
                file = open(filePath, 'rb')
            except:
                return HttpResponse(status=404)
            file = File(file)
            response = FileResponse(file)
            response['Content-Disposition'] = 'attachment'
            return response
        else:
            filePath = 'chat/media/' + str(message.file)
            try:
                file = open(filePath, 'rb')
            except:
                return HttpResponse(status=404)
            file = File(file)
            response = FileResponse(file)
            response['Content-Disposition'] = 'attachment'
            return response


class DocView(View):
    def post(self, request: HttpRequest):
        # 检验字段是否完整
        try:
            title = request.POST.get('title')
            link = request.POST.get('link')
            roomId = request.POST.get('roomId')
            userId = request.POST.get('userId')
        except:
            return HttpResponse({"status":400})

        try:
            room = Room.objects.get(id=roomId)
        except:
            return HttpResponse({"status":404})

        try:
            UserRoom.objects.get(user=userId, room=roomId)
        except:
            return HttpResponse({"status":401})

        Document.objects.create(title=str(title), link=str(link), room=room)
        return HttpResponse({"status":200})

    def delete(self, request: HttpRequest):
        json_obj = json.loads(request.body)
        # 检验字段是否完整
        try:
            docId = json_obj['docId']
            roomId = json_obj['roomId']
        except:
            return HttpResponse({"status":400})

        try:
            UserRoom.objects.get(user=request.userId, room=roomId)
        except:
            return HttpResponse({"status":401})

        try:
            doc = Document.objects.get(id=docId)
        except:
            return HttpResponse({"status":404})

        doc.delete()
        return HttpResponse({"status":200})


class DocListView(View):


    def post(self, request: HttpRequest):
        # 检验字段是否完整
        try:
            roomId = request.POST.get('roomId')
        except:
            return HttpResponse({"status":400})

        try:
            room = Room.objects.get(id=roomId)
        except:
            return HttpResponse({"status":400})

        docs = Document.objects.filter(room=room)
        res_docs = []
        for doc in docs:
            doc = {
                'id': str(doc.id),
                'link': doc.link,
                'title': doc.title
            }
            res_docs.append(doc)
        res = {
            'docs': res_docs
        }
        return HttpResponse(json.dumps(res), status=200, content_type='application/json')
