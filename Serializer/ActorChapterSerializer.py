from .ActorSerializer import ActorSerializer
from .ChapterSerializer import ChapterSerializer
from rest_framework import serializers
from Entity.models.Chapter import Chapter
from Entity.models.Actor import Actor
from Serializer.ChapterSerializer import ChapterSerializer
class ChapterActorsSerializer(serializers.ModelSerializer):
    actors = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Chapter
        fields = '__all__'
    def get_actors(self, obj):
        actorList = Actor.objects.filter(actorchapter_Chapter=obj)
        return ActorSerializer(actorList, many=True).data
class ActorChaptersSerializer(serializers.ModelSerializer):
    chaptes = serializers.SerializerMethodField()

    class Meta:
        model = Actor
        fields = '__all__'
    def get_chaptes(self, obj):
        actorList = Chapter.objects.filter(chapteractor__Actor=obj)
        return ChapterSerializer(actorList, many=True).data

