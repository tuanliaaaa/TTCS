from rest_framework import serializers
from Entity.models.Chapter import Chapter
from Entity.models.Film import Film
from Entity.models.Actor import Actor
from Serializer.ActorSerializer import ActorSerializer
class FilmSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Film
        fields = '__all__'
class ChapterSerializer(serializers.ModelSerializer):
    Film = FilmSerializer(many=False)
    actor = serializers.SerializerMethodField()
    class Meta:
        model = Chapter
        fields = '__all__'
    def get_actor(self, obj):
        actorList = Actor.objects.filter(actorchapter__Chapter=obj)
        return ActorSerializer(actorList, many=True).data

