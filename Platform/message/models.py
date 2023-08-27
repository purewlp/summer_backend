from django.db import models

# Create your models here.


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=512, null=True)

    # False 未读  True 已读
    status = models.BooleanField(default=False)
    publisher = models.CharField(default='System', max_length=64)

    class Meta:
        db_table = 'message'


class UserMessage(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    message = models.ForeignKey('message.Message', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_message'
