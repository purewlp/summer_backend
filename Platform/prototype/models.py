from django.db import models

# Create your models here.


class Prototype(models.Model):
    id = models.CharField(primary_key=True, max_length=256)
    componentData = models.TextField(null=True)
    canvasStyleData = models.TextField()
    title = models.CharField(max_length=64, default='title')


    class Meta:
        db_table = 'prototype'


class ProjectPrototype(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE)
    prototype = models.ForeignKey('prototype.Prototype', on_delete=models.CASCADE)

    class Meta:
        db_table = 'project_prototype'












