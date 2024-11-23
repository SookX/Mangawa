from django.db import models
from user.models import CustomUser

class Progress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    weight = models.FloatField()
    image = models.ImageField(upload_to='progress_images/', max_length=500)
    height = models.FloatField()
    date = models.DateField(auto_now_add=True)


