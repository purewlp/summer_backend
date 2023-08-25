from django.db import models

# Create your models here.

class User(models.Model):
    username=models.CharField("name",max_length=100)
    password = models.CharField("password",max_length=20)
    realname=models.CharField("realname",max_length=20,null=True)
    nickname=models.CharField("nickname",max_length=20,null=True)
    email = models.CharField("email",max_length=30,null=True)

    class Meta:
        db_table = 'user'

class VerificationCode_info(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField("code",max_length=6,null=True)
    expiration_time = models.DateTimeField()

    def __str__(self):
        return self.email
    class Meta:
        db_table='VerificationCode_info'
