from rest_framework import serializers
from Entity.models.User import User
from Entity.models.Chapter import Chapter
from Entity.models.History import History
from .UserSerializer import UserSerializer
from .ChapterSerializer import ChapterSerializer
class UserChaptersSerializer(serializers.ModelSerializer):
    chapters = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'
    def get_chapters(self, obj):
        chapterList = Chapter.objects.filter(chapteruser__User=obj)
        return ChapterSerializer(chapterList, many=True).data
class ChapterUsersSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = '__all__'
    def get_users(self, obj):
        userList = User.objects.filter(userchapter__Chapter=obj)
        return UserSerializer(userList, many=True).data
class HistorySerializer(serializers.ModelSerializer):
    User = UserSerializer()
    Chapter =ChapterSerializer()
    class Meta:
        model = History
        fields = '__all__'
