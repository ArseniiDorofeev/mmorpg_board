# Generated by Django 5.0.1 on 2024-01-14 20:46

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mmorpg_board_app', '0002_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', ckeditor.fields.RichTextField()),
                ('image1', models.ImageField(blank=True, null=True, upload_to='advertisement_images/')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='advertisement_images/')),
                ('video1', models.URLField(blank=True, null=True)),
                ('video2', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
