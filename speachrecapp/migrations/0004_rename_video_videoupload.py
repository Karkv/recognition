# Generated by Django 5.0 on 2024-04-01 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('speachrecapp', '0003_rename_video_video_videos'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='video',
            new_name='videoupload',
        ),
    ]
