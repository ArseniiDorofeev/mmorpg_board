# Generated by Django 5.0.1 on 2024-01-18 14:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('mmorpg_board_app', '0007_alter_advertisement_author_response_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertisement',
            name='responses',
        ),
        migrations.AddField(
            model_name='response',
            name='receiver',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='received_responses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AlterField(
            model_name='response',
            name='advertisement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='mmorpg_board_app.advertisement'),
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
