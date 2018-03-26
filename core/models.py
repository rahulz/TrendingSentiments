from django.db import models

# Create your models here.
from django.db.models import CASCADE


class Trend(models.Model):
    name = models.TextField(primary_key=True)
    query = models.TextField()
    tweet_volume = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_at_date = models.DateField(auto_now_add=True)


class Tweet(models.Model):
    trend = models.ForeignKey(Trend, on_delete=CASCADE)
    text = models.TextField()
    cleaned_text = models.TextField()
    id = models.TextField(primary_key=True)
    polarity = models.FloatField()
    subjectivity = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_at_date = models.DateField(auto_now_add=True)
