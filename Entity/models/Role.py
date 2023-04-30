from django.db import models
class Role(models.Model):
    RoleName = models.CharField(max_length=255)