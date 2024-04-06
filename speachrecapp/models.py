from django.db import models
# from django.contrib.postgres.fields import JSONField

# Create your models here.

class voicerec(models.Model):
    caption=models.CharField(max_length=199)
    videos=models.FileField(upload_to="videos/",null=True,default=None)
    VideoTitle=models.CharField(max_length=100)
    audia=models.FileField(upload_to='',null=True,default=None)
    audioTitle=models.CharField(max_length=100)
    filter_words=models.JSONField()
    sentiment_scores=models.JSONField()
    sentiment_scores_compound=models.CharField(max_length=100)
    sentiment_scores_average=models.FloatField()
    RMS=models.CharField(max_length=100)
    RMS_threshold=models.CharField(max_length=100)
    Pitch=models.IntegerField()
    percentage_modulation=models.CharField(max_length=100)
    Modulation_rating=models.CharField(max_length=100)
    

    def __str__(self):
        return self.caption
    
class videoupload(models.Model):
    caption=models.CharField(max_length=199)
    videos=models.FileField(upload_to="videos/",null=True,default=None)

    def __str__(self):
        return self.caption