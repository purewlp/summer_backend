# Generated by Django 4.2.4 on 2023-08-27 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prototype', '0003_remove_prototype_all_alter_prototype_canvasstyledata_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prototype',
            name='id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]