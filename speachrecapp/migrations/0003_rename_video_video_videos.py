# Generated by Django 5.0 on 2024-04-01 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('speachrecapp', '0002_alter_video_video'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='video',
            new_name='videos',
        ),
    ]
