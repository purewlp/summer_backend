from django.db import models
from team.models import Team
from user.models import User
from django.utils import timezone

# Create your models here.

class Project(models.Model):
    name=models.CharField(max_length=100)
    creator=models.ForeignKey(User,on_delete=models.CASCADE)
    team=models.ForeignKey(Team,on_delete=models.CASCADE)
    created_time=models.DateTimeField(null=True)
    finished=models.BooleanField(default=False)
    finished_time=models.DateTimeField(null=True,blank=True)
    
    def save(self, *args, **kwargs):
        # 如果项目ID尚未分配，分配一个从10001开始的唯一项目ID
        if not self.created_time:
            self.created_time=timezone.now()
        if self.id is None:
            last_project = Project.objects.order_by('-id').first()
            if last_project:
                self.id = last_project.id + 1
            else:
                self.id = 10001
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name
    class Meta:
        db_table='project'

class ProjectRecycleBin(models.Model):
    name=models.CharField(max_length=100)
    deleter_id=models.BigIntegerField(null=True)
    creator_id=models.BigIntegerField(null=True)
    team=models.ForeignKey(Team,on_delete=models.CASCADE,null=True)
    project_id=models.BigIntegerField(null=True)
    created_time=models.DateTimeField(null=True)
    finished=models.BooleanField(default=False)
    finished_time=models.DateTimeField(null=True,blank=True)
    deleted_time=models.DateTimeField(auto_now_add=True,null=True)
    expiration_time=models.DateTimeField(null=True)
    def save(self, *args, **kwargs):
        # 如果项目ID尚未分配，分配一个从10001开始的唯一项目ID
        if self.deleted_time is None:
            self.deleted_time = timezone.now()
        if not self.expiration_time:
            self.expiration_time = self.deleted_time + timezone.timedelta(minutes=10)
        if self.id is None:
            last_project = ProjectRecycleBin.objects.order_by('-id').first()
            if last_project:
                self.id = last_project.id + 1
            else:
                self.id = 10001
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name
    class Meta:
        db_table='project_recyclebin'

class Collection(models.Model):
    team=models.ForeignKey(Team,on_delete=models.CASCADE)
    project_id=models.BigIntegerField(null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        # 如果项目ID尚未分配，分配一个从10001开始的唯一项目ID
        if self.id is None:
            last_project = Collection.objects.order_by('-id').first()
            if last_project:
                self.id = last_project.id + 1
            else:
                self.id = 1
        super().save(*args,**kwargs)


