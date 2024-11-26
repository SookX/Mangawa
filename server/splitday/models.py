from django.db import models
from user.models import CustomUser

class SplitDay(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)

class Exercise(models.Model):
    splitDay = models.ForeignKey(SplitDay, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=False)

class KgAndReps(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    kg = models.FloatField()
    reps = models.FloatField()
    date = models.DateField(auto_now_add=False)