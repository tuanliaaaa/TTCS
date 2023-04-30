from rest_framework import serializers
from Entity.models.Role import Role
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }
        
