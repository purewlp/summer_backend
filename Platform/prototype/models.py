from django.db import models

# Create your models here.


class Prototype(models.Model):
    id = models.CharField(primary_key=True, max_length=256)
    componentData = models.TextField()
    canvasStyleData = models.TextField()
    title = models.CharField(max_length=64, default='title')


    class Meta:
        db_table = 'prototype'













