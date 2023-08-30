from django.db import models


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, null=True)
    team = models.ForeignKey('team.Team', on_delete=models.CASCADE)
    rank = models.IntegerField(default=0)
    groupMakerId = models.IntegerField(null = True)
    class Meta:
        db_table = 'room'




class ChatMessage(models.Model):
    id = models.AutoField(primary_key=True)
    isImage = models.BooleanField()
    content = models.TextField(null=True)
    sentTime = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='chatImage', null=True)
    file = models.FileField(upload_to='chatFile', null=True)
    auther = models.ForeignKey('user.User', on_delete=models.CASCADE)
    room = models.ForeignKey('chat.Room', on_delete=models.CASCADE)
    isEmoji = models.BooleanField(default=False)
    class Meta:
        db_table = 'chatMessage'


class UserRoom(models.Model):
    room = models.ForeignKey('chat.Room', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    class Meta:
        db_table = 'user_room'


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256)
    link = models.CharField(max_length=256)
    room = models.ForeignKey('chat.Room', on_delete=models.CASCADE)

    class Meta:
        db_table = 'chat_document'
