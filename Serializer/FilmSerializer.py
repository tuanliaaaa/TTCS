from rest_framework import serializers
from django.db import transaction
from Entity.models.Film import Film
from Entity.models.Chapter import Chapter
from Serializer.ChapterSerializer import ChapterSerializer
class ChapterSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Chapter
        fields = '__all__'
class FilmSerializer(serializers.ModelSerializer):
    
    chapters = ChapterSerializer(many=True, read_only=True)
    class Meta:
        model = Film
        fields = '__all__'

    # def to_internal_value(self, data):
        
    #     return data
    # # def validate(self, data):
    # #     additional_param_1 = self.context.get('additional_param_1')
    # #     return data
    # @transaction.atomic
    # def create(self, validated_data):
    #     print(validated_data)
    #     chapters_data = validated_data.pop('ListCategory')
    #     # print(validated_data)
    #     film = Film.objects.create(**validated_data)
    #     # for chapter_data in chapters_data:
    #     #     Chapter.objects.create(film=film, **chapter_data)
    #     return film
