from django.db import models
class Actor(models.Model):
    ActorName = models.CharField(max_length=255)
    Age = models.IntegerField()
    nativeLand =models.CharField(max_length=225)
    Sex =models.BooleanField()