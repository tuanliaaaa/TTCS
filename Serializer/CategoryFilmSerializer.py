from .CategorySerializer import CategorySerializer
from .FilmSerializer import FilmSerializer
from rest_framework import serializers
from Entity.models.Film import Film
from Entity.models.Category import Category
from Serializer.ChapterSerializer import ChapterSerializer
class FilmCategorysSerializer(serializers.ModelSerializer):
    categorys = serializers.SerializerMethodField()
    chapters = ChapterSerializer(many=True, read_only=True)
    
    class Meta:
        model = Film
        fields = '__all__'
    def get_categorys(self, obj):
        categoryList = Category.objects.filter(categoryfilm__Film=obj)
        return CategorySerializer(categoryList, many=True).data
class CategoryFilmsSerializer(serializers.ModelSerializer):
    films = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'
    def get_films(self, obj):
        filmList = Film.objects.filter(filmcategory__Category=obj)
        return FilmSerializer(filmList, many=True).data

