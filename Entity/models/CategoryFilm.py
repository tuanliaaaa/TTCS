from django.db import models
from .Category import Category
from .Film import Film
class CategoryFilm(models.Model):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='categoryfilm')
    Film = models.ForeignKey(Film, on_delete=models.CASCADE,related_name='filmcategory')
    