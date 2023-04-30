from rest_framework import serializers
from Entity.models.Actor import Actor
class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }
        
