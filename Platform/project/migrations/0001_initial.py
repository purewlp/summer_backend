# Generated by Django 4.2.4 on 2023-08-27 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('team', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectRecycleBin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('deleter_id', models.BigIntegerField(null=True)),
                ('creator_id', models.BigIntegerField(null=True)),
                ('project_id', models.BigIntegerField(null=True)),
                ('created_time', models.DateTimeField(null=True)),
                ('finished', models.BooleanField(default=False)),
                ('finished_time', models.DateTimeField(blank=True, null=True)),
                ('deleted_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('expiration_time', models.DateTimeField(null=True)),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='team.team')),
            ],
            options={
                'db_table': 'project_recyclebin',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_time', models.DateTimeField(null=True)),
                ('finished', models.BooleanField(default=False)),
                ('finished_time', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.team')),
            ],
            options={
                'db_table': 'project',
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.BigIntegerField(null=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]
