from django.http import JsonResponse
from django.shortcuts import render

from message.models import UserMessage, Message
from user.models import User


# Create your views here.

def message(request):
    if request.method == 'GET':
        userId = request.GET.get('userId')
        user = User.objects.get(id=userId)
        userMessages = UserMessage.objects.filter(user=user)
        unread = []
        for userMessage in userMessages:
            message = userMessage.message
            if not message.status:
                unread.append({
                    'time': message.time,
                    'content': message.content,
                    'link': message.link,
                    'messageId': message.id
                })

        return JsonResponse({'errno': 0, 'unread': unread})

    else:
        return JsonResponse({'errno': 1001})


def readMessage(request):
    if request.method == 'GET':
        userId = request.GET.get('userId')
        user = User.objects.get(id=userId)
        userMessages = UserMessage.objects.filter(user=user)
        read = []
        for userMessage in userMessages:
            message = userMessage.message
            if message.status:
                read.append({
                    'time': message.time,
                    'content': message.content,
                    'link': message.link,
                    'messageId': message.id
                })

        return JsonResponse({'errno': 0, 'read': read})

    else:
        return JsonResponse({'errno': 1001})


def deleteMessage(request):
    if request.method == 'POST':
        messageId = request.POST.get('messageId')
        try:
            message = Message.objects.get(id=messageId)
        except:
            return JsonResponse({'errno': 1002})
        message.delete()
        return JsonResponse({'errno': 0})

    else:
        return JsonResponse({'errno': 1001})


def changeMessage(request):
    if request.method == "POST":
        messageId = request.POST.get('messageId')
        try:
            message = Message.objects.get(id=messageId)
        except:
            return JsonResponse({'errno': 1002})
        message.status = True
        message.save()
        return JsonResponse({'errno': 0})

    else:
        return JsonResponse({'errno': 1001})


def deleteAllMessage(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        user = User.objects.get(id=userId)
        userMessages = UserMessage.objects.filter(user=user)
        for userMessage in userMessages:
            message = userMessage.message
            if message.status:
                message.delete()

        return JsonResponse({'errno': 0})

    else:
        return JsonResponse({'errno': 1001})


def changeAllMessage(request):
    if request.method == "POST":
        userId = request.POST.get('userId')
        user = User.objects.get(id=userId)
        try:
            userMessages = UserMessage.objects.filter(user=user)
        except:
            return JsonResponse({'errno': 1002})
        for userMessage in userMessages:
            message = userMessage.message
            if not message.status:
                message.status = True
                message.save()

        return JsonResponse({'errno': 0})

    else:
        return JsonResponse({'errno': 1001})


def sendMessage(request):
    if request.method == 'POST':
        groupId = request.POST.get('groupId')
        userId = request.POST.get('userId')
        content = request.POST.get('content')
        publiserId = request.POST.get('id')

        try:
            user = User.objects.get(id=userId)
            message = Message(content=content, publisher=publiserId)
            message.save()
            user_message = UserMessage(user=user, message=message)
            user_message.save()
            return JsonResponse({'errno': 0})
        except:
            return JsonResponse({'errno': 1002})

    else:
        return JsonResponse({'errno': 1001})











