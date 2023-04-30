from django.db import models
class Category(models.Model):
    CategoryName = models.CharField(max_length=255)