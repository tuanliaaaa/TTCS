from rest_framework import serializers
from Entity.models.User import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
        extra_kwargs = {
            'id': {'read_only': True},
            'Password': {'write_only': True},
            'UserName': {'read_only': True}
        }
class UserByAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
       
