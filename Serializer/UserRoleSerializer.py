from .RoleSerializer import RoleSerializer
from .UserSerializer import UserSerializer
from rest_framework import serializers
from Entity.models.Role import Role
from Entity.models.User import User
class UserRolesSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'
    def get_roles(self, obj):
        roleList = Role.objects.filter(roleuser__User=obj)
        return RoleSerializer(roleList, many=True).data
class RoleUsersSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = '__all__'
    def get_users(self, obj):
        userList = User.objects.filter(userrole__Role=obj)
        return UserSerializer(userList, many=True).data
