from django.db import models
from project.models import Project
from user.models import User
from django.utils import timezone

# Create your models here.
class Folder(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=20,null=True,default="新建文件夹")

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if self.id is None:
            # 如果 ID 为空，为其分配一个从 1 开始的值
            last_folder = Folder.objects.order_by('-id').first()
            if last_folder:
                self.id = last_folder.id + 1
            else:
                self.id = 1
        super().save(*args, **kwargs)


class Document(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=20,null=True,default="新建文档")
    content=models.TextField(null=True)
    creator=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    created_time=models.DateTimeField(null=True)
    edited_time=models.DateTimeField(null=True)
    folder=models.ForeignKey(Folder,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.created_time:
            self.created_time=timezone.now()
        if not self.edited_time:
            self.edited_time=timezone.now()
        if self.id is None:
            # 如果 ID 为空，为其分配一个从 1 开始的值
            last_document = Document.objects.order_by('-id').first()
            if last_document:
                self.id = last_document.id + 1
            else:
                self.id = 1

        super().save(*args, **kwargs)

    class Meta:
        db_table='document'

class DocumentVersion(models.Model):
    name=models.CharField(max_length=20,null=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    edited_time=models.DateTimeField(null=True)
    version=models.PositiveIntegerField(default=0)
    # editor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.content
    def save(self, *args, **kwargs):
        if not self.edited_time:
            self.edited_time=timezone.now()
        if self.id is None:
            # 如果 ID 为空，为其分配一个从 1 开始的值
            last_version = DocumentVersion.objects.order_by('-id').first()
            if last_version:
                self.id = last_version.id + 1
            else:
                self.id = 1

        last_version = DocumentVersion.objects.filter(document=self.document).order_by('-version').first()
        if last_version:
            self.version = last_version.version + 1

        super().save(*args, **kwargs)

    class Meta:
        db_table='document_version'
