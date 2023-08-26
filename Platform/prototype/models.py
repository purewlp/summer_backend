from django.db import models

# Create your models here.


class Prototype(models.Model):
    id = models.AutoField(primary_key=True)
    componentData = models.CharField(max_length=255)
    canvasStyleData = models.CharField(max_length=256)
    all = models.CharField(max_length=4096)
    title = models.CharField(max_length=64, default='title')


    class Meta:
        db_table = 'prototype'













