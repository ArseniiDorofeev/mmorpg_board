# Generated by Django 5.0.1 on 2024-01-15 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mmorpg_board_app', '0003_advertisement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]