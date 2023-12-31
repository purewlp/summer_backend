# Generated by Django 4.2.4 on 2023-09-03 00:20

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, verbose_name='name')),
                ('password', models.CharField(max_length=20, verbose_name='password')),
                ('realname', models.CharField(max_length=20, null=True, verbose_name='realname')),
                ('nickname', models.CharField(max_length=20, null=True, verbose_name='nickname')),
                ('email', models.CharField(max_length=30, null=True, verbose_name='email')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=user.models.User.user_directory_path, verbose_name='avatar')),
                ('avatar_url', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='VerificationCode_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('code', models.CharField(max_length=6, null=True, verbose_name='code')),
                ('expiration_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'VerificationCode_info',
            },
        ),
    ]
