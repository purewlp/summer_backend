# Generated by Django 4.2.4 on 2023-08-27 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0017_collection'),
        ('prototype', '0002_prototype_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prototype',
            name='all',
        ),
        migrations.AlterField(
            model_name='prototype',
            name='canvasStyleData',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='prototype',
            name='componentData',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='prototype',
            name='id',
            field=models.CharField(max_length=256, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='ProjectPrototype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project')),
                ('prototype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prototype.prototype')),
            ],
            options={
                'db_table': 'project_prototype',
            },
        ),
    ]