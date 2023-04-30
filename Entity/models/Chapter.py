from django.db import models
from .Film import Film
class Chapter(models.Model):
    Film = models.ForeignKey(Film,related_name='chapters', on_delete=models.CASCADE)
    ChapterName = models.CharField(max_length=255,blank=True)
    ChapterDescription = models.TextField()
    ChapterNumber = models.IntegerField()
    Video = models.TextField()
    TrailerChapter= models.TextField()
    ChapterImage = models.CharField(max_length=225)
    ChapterStatus = models.CharField(max_length=225)
    ChapterCreateDay = models.DateTimeField(auto_now_add=True,null=True)
    ChapterPremieredDay = models.DateTimeField(blank=True,null=True)
    def save(self, *args, **kwargs):
        if not self.id:
            try:
                self.ChapterNumber = Chapter.objects.filter(Film=self.Film).order_by("-ChapterNumber")[0].ChapterNumber+1
            except:
                self.ChapterNumber=1
        super().save(*args, **kwargs)
    
    