from django.db import models
from enum import Enum
from user.models import User

# Create your models here.

class RoleEnum(Enum):
    CREATOR = '创建者'
    ADMIN = '管理员'
    MEMBER = '成员'

class Team(models.Model):
    name=models.CharField(max_length=100)
    creator=models.ForeignKey(User,on_delete=models.CASCADE,related_name='teams_created')
    members = models.ManyToManyField(User,through='Membership')

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if self.id is None:
            # 如果 ID 为空，为其分配一个从 1 开始的值
            last_team = Team.objects.order_by('-id').first()
            if last_team:
                self.id = last_team.id + 1
            else:
                self.id = 1

        super().save(*args, **kwargs)

        if self.id is not None:
            # 创建 Team 成功后，创建相应的 Membership 记录
            Membership.objects.create(user=self.creator, team=self, role=RoleEnum.CREATOR.value)
    class Meta:
        db_table='team'

class Membership(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    team=models.ForeignKey(Team,on_delete=models.CASCADE)
    role=models.CharField(max_length=20,choices=[(role.value, role.name) for role in RoleEnum], default=RoleEnum.MEMBER.value)

    def __str__(self):
        return f'{self.user.username} in {self.team.name} as {self.role}'
    def save(self, *args, **kwargs):
        if self.id is None:
            # 如果 ID 为空，为其分配一个从 1 开始的值
            last_membership = Membership.objects.order_by('-id').first()
            if last_membership:
                self.id = last_membership.id + 1
            else:
                self.id = 1

        super().save(*args, **kwargs)
    class Meta:
        db_table='membership'

class Invitation(models.Model):
    team=models.ForeignKey(Team,on_delete=models.CASCADE)
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations_sent',null=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations_received',null=True)
    def save(self,*args,**kwargs):
        if self.id is None:
            # 如果 ID 为空，为其分配一个从 1 开始的值
            last_invitation = Invitation.objects.order_by('-id').first()
            if last_invitation:
                self.id = last_invitation.id + 1
            else:
                self.id = 1

        super().save(*args, **kwargs)