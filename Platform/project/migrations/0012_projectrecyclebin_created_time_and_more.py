# Generated by Django 4.2.4 on 2023-08-26 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_projectrecyclebin_deleted_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectrecyclebin',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='projectrecyclebin',
            name='finished',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='projectrecyclebin',
            name='finished_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]