# Generated by Django 4.2.4 on 2023-08-27 22:28

from django.db import migrations, models
import team.models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=team.models.Team.team_directory_path, verbose_name='avatar'),
        ),
    ]
