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


class MessageView(View):
    # 聊天室历史消息
    def post(self, request: HttpRequest):
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
        memberShip = Membership.objects.get(user=user, team=room.team)

        if room.rank == 1 :
            if room.groupMakerId == user.id:
                permission = "创建者"
            else:
                permission = "成员"
        else:
            permission = memberShip.role
        ans = {
            "messages": [],
            "permission": permission,
        }
        for message in ChatMessage.objects.filter(room=room):
            if message.isImage:
                image = 'http://43.143.140.26/'+'media/' + str(message.image)
                content = ''
                file = ''
                fileName = str(image).split("/")[len(str(image).split("/")) - 1]
                type = 'image'
            else:
                if message.content is not None:
                    if message.isEmoji is False:
                        content = message.content
                        image = ''
                        file = ''
                        fileName = ''
                        type = 'text'
                    else:
                        content = message.content
                        image = ''
                        file = ''
                        fileName = ''
                        type = 'emoji'
                else:
                    content = ''
                    image = ''
                    file = 'http://43.143.140.26/'+'media/' + str(message.file)
                    fileName = message.fileName
                    type = 'file'
            sub_ans = {
                "id": str(message.id),
                "authorId": str(message.auther.id),
                "type": str(type),
                "content": str(content),
                "authorName": str(message.auther.nickname),
                "avatar": str(message.auther.avatar_url),
                "time": str(message.sentTime.strftime("%Y-%m-%d %H:%M:%S")),
                "image": str(image),
                "file": str(file),
                "fileName": str(fileName),
                "fileType": str(message.fileType)
            }
            ans['messages'].append(sub_ans)
        return HttpResponse(json.dumps(ans), content_type='application/json', status=200)


class RoomList(View):
    # 获取聊天室列表

    def post(self, request: HttpRequest):
        groupId = request.POST.get('groupId')
        userId = request.POST.get('userId')
        try:
            user = User.objects.get(id=userId)
            if int(groupId) != 0:
                print(1111)
                team = Team.objects.get(id = groupId)
        except:
            return HttpResponse(status=401)
        userRooms = UserRoom.objects.filter(user=user)
        rooms = {
            "teamRooms":[],
            "groupRooms":[],
            "personalRooms":[]
        }
        print(groupId)
        if int(groupId) == 0:
            for userRoom in userRooms:
                if userRoom.room.rank == 1:
                    groupRoom = {
                        'roomName': str(userRoom.room.name),
                        'roomId': str(userRoom.room.id),
                        'team': str(userRoom.room.team),
                        'headImg': "https://img0.baidu.com/it/u=2626931382,2326744140&fm=253&fmt=auto&app=138&f=JPEG?w=400&h=400"
                    }
                    rooms["groupRooms"].append(groupRoom)
            return HttpResponse(json.dumps(rooms), content_type='application/json', status=200)
        else:
            for userRoom in userRooms:
                if userRoom.room.rank == 0 and userRoom.room.team == team:
                    teamRoom = {
                        'roomName': str(userRoom.room.name),
                        'roomId': str(userRoom.room.id),
                        'team': str(userRoom.room.team),
                        'headImg': "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fc-ssl.duitang.com%2Fuploads%2Fitem%2F202007%2F15%2F20200715133648_FUVdd.jpeg&refer=http%3A%2F%2Fc-ssl.duitang.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1695967288&t=9a2bb0340d7902d0721d4ac2a0b328ba"
                    }
                    rooms["teamRooms"].append(teamRoom)
                elif userRoom.room.rank == 2 and userRoom.room.team == team:
                    others = UserRoom.objects.filter(room=userRoom.room)
                    for other in others:
                        if other.user.id !=userId:
                            roomName = str(other.user.nickname)
                            break
                    personalRoom = {
                        'roomName': roomName,
                        'roomId': str(userRoom.room.id),
                        'team': str(userRoom.room.team),
                        'headImg': "https://img2.baidu.com/it/u=2363754754,1104567454&fm=253&fmt=auto&app=138&f=JPEG?w=400&h=400"
                    }
                    rooms["personalRooms"].append(personalRoom)
            return HttpResponse(json.dumps(rooms), content_type='application/json', status=200)


class FileView(View):
    def post(self, request: HttpRequest):
        try:
            messageId = request.POST.get('roomId')
        except:
            return HttpResponse(status=400)
        message = ChatMessage.objects.get(id=messageId)
        if message.isImage:
            filePath = 'media/' + str(message.image)
            try:
                file = open(filePath, 'rb')
            except:
                return HttpResponse(status=404)
            file = File(file)
            response = FileResponse(file)
            response['Content-Disposition'] = 'attachment'
            return response
        else:
            filePath = 'media/' + str(message.file)
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
            return HttpResponse({"status": 400})

        try:
            room = Room.objects.get(id=roomId)
        except:
            return HttpResponse({"status": 404})

        try:
            UserRoom.objects.get(user=userId, room=roomId)
        except:
            return HttpResponse({"status": 401})

        Document.objects.create(title=str(title), link=str(link), room=room)
        return HttpResponse({"status": 200})

    def delete(self, request: HttpRequest):
        json_obj = json.loads(request.body)
        # 检验字段是否完整
        try:
            docId = json_obj['docId']
            roomId = json_obj['roomId']
        except:
            return HttpResponse({"status": 400})

        try:
            UserRoom.objects.get(user=request.userId, room=roomId)
        except:
            return HttpResponse({"status": 401})

        try:
            doc = Document.objects.get(id=docId)
        except:
            return HttpResponse({"status": 404})

        doc.delete()
        return HttpResponse({"status": 200})


class DocListView(View):

    def post(self, request: HttpRequest):
        # 检验字段是否完整
        try:
            roomId = request.POST.get('roomId')
        except:
            return HttpResponse({"status": 400})

        try:
            room = Room.objects.get(id=roomId)
        except:
            return HttpResponse({"status": 400})

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


class GroupMakeView(View):
    def post(self, request: HttpRequest):
        try:
            teamId = request.POST.get('teamId')
            userId = request.POST.get('userId')
            groupName = request.POST.get('groupName')
        except:
            return HttpResponse({"errno":"传入数据有误"})
        try:
            team = Team.objects.get(id=teamId)
            user = User.objects.get(id=userId)
        except:
            return HttpResponse({"errno":"找不到嘞"})
        newRoom =Room.objects.create(team=team, rank=1,groupMakerId=user.id,name=groupName)
        newUserRoom = UserRoom.objects.create(user=user,room=newRoom)
        return HttpResponse({"status": 200})

class GroupInviteView(View):
    def post(self, request: HttpRequest):
        try:
            roomId = request.POST.get('roomId')
            userId = request.POST.get('userId')
            invites = request.POST.getlist('invite[]')
            print(invites)
        except:
            return HttpResponse({"errno":"你发的什么东西"})
        try:
            user = User.objects.get(id=userId)
            room = Room.objects.get(id=roomId)
            invites=list(invites)
            for invite in invites:
                print(invite)
                invited = User.objects.get(id=invite)
                UserRoom.objects.create(room=room, user=invited)
        except:
            return HttpResponse({"errno":"根本找不到"},status=400)
        return HttpResponse({"status": 200})

class RoomRemoveView(View):
    def post(self, request: HttpRequest):
        try:
            roomId = request.POST.get('roomId')
            userId = request.POST.get('userId')
        except:
            return HttpResponse({"errno": "你发的什么东西"})
        try:
            user = User.objects.get(id=userId)
            room = Room.objects.get(id=roomId)
        except:
            return HttpResponse({"errno":"根本找不到"},status=400)
        UserRoom.objects.filter(room=room).all().delete()
        Room.objects.filter(id=roomId).all().delete()
        return HttpResponse({"status": 200})

class GroupDeleteView(View):
    def post(self, request: HttpRequest):
        try:
            roomId = request.POST.get('roomId')
            userId = request.POST.get('userId')
            delId = request.POST.get('delete')
        except:
            return HttpResponse({"errno": "你发的什么东西"})
        try:
            user = User.objects.get(id=userId)
            room = Room.objects.get(id=roomId)
            dels = User.objects.get(id=delId)
        except:
            return HttpResponse({"errno":"根本找不到"},status=400)
        UserRoom.objects.get(room=room,user=dels).delete()
        return HttpResponse({"status": 200})

class RoomView(View):
    def post(self, request: HttpRequest):
        try:
            roomId = request.POST.get('roomId')
            userId = request.POST.get('userId')
        except:
            return HttpResponse({"errno": "你发的什么东西"})
        try:
            room = Room.objects.get(id=roomId)
            leader = User.objects.get(id= userId)
        except:
            return HttpResponse({"errno":"根本找不到"},status=400)
        if room.rank ==0:
            try:
                role = Membership.objects.get(user=leader,team=room.team).role
            except:
                return HttpResponse({"errno": "根本找不到"}, status=400)
        elif room.rank ==2:
            role = "成员"
        else:
            if int(room.groupMakerId) == int(userId):
                role = "创建者"
            else:
                role = '成员'
        identity = {
            "role": str(role),
            "members": [],
        }
        userRooms = UserRoom.objects.filter(room=room)
        users = []
        for userRoom in userRooms:
            users.append(userRoom.user)
        for user in users:
            if room.rank == 0:
                role = Membership.objects.get(user=user, team=room.team).role
            elif room.rank == 2:
                role = "成员"
            else:
                if room.groupMakerId == user.id:
                    role = "创建者"
                else:
                    role = '成员'
            member_data = {
                "id": user.id,
                "role": str(role),
                "nickname": user.nickname,
                "realname": user.realname,
                "email": user.email,
                "avatar": user.avatar_url,
            }
            identity["members"].append(member_data)

        return HttpResponse(json.dumps(identity), content_type='application/json', status=200)
