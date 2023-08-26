# Generated by Django 4.2.4 on 2023-08-27 00:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0017_collection'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, null=True)),
                ('project_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.project')),
            ],
            options={
                'db_table': 'document',
            },
        ),
    ]
