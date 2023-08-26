from django.db import models
from project.models import Project

# Create your models here.
class Document(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=20,null=True,default="新建文档")

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
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