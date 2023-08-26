# Generated by Django 4.2.4 on 2023-08-26 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_alter_user_avatar'),
        ('team', '0003_remove_invitation_user_invitation_inviter_and_more'),
        ('project', '0004_rename_creator_projectrecyclebin_deleter_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectrecyclebin',
            name='deleter',
        ),
        migrations.AddField(
            model_name='projectrecyclebin',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
        migrations.AddField(
            model_name='projectrecyclebin',
            name='deleter_id',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='projectrecyclebin',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='team.team'),
        ),
    ]
