# Generated by Django 5.0 on 2024-04-04 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speachrecapp', '0005_voicerec'),
    ]

    operations = [
        migrations.AddField(
            model_name='voicerec',
            name='sentiment_scores_average',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
