from django.db import models
from .Actor import Actor
from .Chapter import Chapter
class ActorChapter(models.Model):
    Actor = models.ForeignKey(Actor,on_delete=models.CASCADE,related_name='actorchapter')
    Chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE,related_name='chapteractor')