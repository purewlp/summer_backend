# Generated by Django 4.2.4 on 2023-08-31 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_project_copynum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectrecyclebin',
            name='id',
        ),
    ]
