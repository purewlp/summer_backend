from django.db import models
from django.utils.text import slugify
# Create your models here.

class User(models.Model):
    username=models.CharField("name",max_length=100)
    password = models.CharField("password",max_length=20)
    realname=models.CharField("realname",max_length=20,null=True)
    nickname=models.CharField("nickname",max_length=20,null=True)
    email = models.CharField("email",max_length=30,null=True)
    def user_directory_path(instance, filename):
        # 生成以用户ID命名的子目录，确保文件名不会冲突
        return f'avatars/user_{instance.id}/{filename}'
    avatar=models.ImageField("avatar",upload_to=user_directory_path,null=True,blank=True)
    def save(self, *args, **kwargs):
        if self.id is None:
            # 如果 ID 为空，为其分配一个从 1 开始的值
            last_user = User.objects.order_by('-id').first()
            if last_user:
                self.id = last_user.id + 1
            else:
                self.id = 1

        super().save(*args, **kwargs)
    class Meta:
        db_table = 'user'

class VerificationCode_info(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField("code",max_length=6,null=True)
    expiration_time = models.DateTimeField()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.id is None:
            # 如果 ID 为空，为其分配一个从 1 开始的值
            last_info = VerificationCode_info.objects.order_by('-id').first()
            if last_info:
                self.id = last_info.id + 1
            else:
                self.id = 1

        super().save(*args, **kwargs)
    class Meta:
        db_table='VerificationCode_info'
