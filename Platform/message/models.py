from django.db import models
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

# Create your models here.


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=512, null=True)
    isInvited = models.BooleanField(default=False)
    invitation = models.ForeignKey('team.Invitation', on_delete=models.CASCADE, null=True)

    # False 未读  True 已读
    status = models.BooleanField(default=False)
    publisher = models.CharField(default='System', max_length=64)




    class Meta:
        db_table = 'message'


class UserMessage(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    message = models.ForeignKey('message.Message', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        message = {"message": '消息已保存'}

        userId = self.user.id

        async def send_update():
            await channel_layer.group_send("user_message", {
                "type": "send.update",
                "message": message,
                "userId": userId
            })

        async_to_sync(send_update)()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'user_message'
