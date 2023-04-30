from django.db import models
class Film(models.Model):
    FilmName = models.CharField(max_length=255)
    FilmDescription = models.TextField()
    BannerFilmName = models.TextField()
    TrailerFilm = models.TextField()
    FilmBollen = models.BooleanField(default=True)
    FilmImage = models.CharField(max_length=225,)
    
    