from Entity.models.User import User
from Entity.models.Chapter import Chapter
from Entity.models.History import History
from rest_framework.views import APIView
from rest_framework.response import Response
from Serializer.HistorySerializer import UserChaptersSerializer,HistorySerializer
import jwt
from datetime import datetime
from core.roleLoginDecorater import RoleRequest
from django.utils.decorators import method_decorator
from core.settings import SECRET_KEY
class HistoryUserLogin(APIView):
    @method_decorator(RoleRequest(allowedRoles=['Admin','NormalUser']))
    def get(self,request):
        try:
            historyUserLogin = User.objects.get(pk=request.userID)
            historyUserLoginJson = UserChaptersSerializer(historyUserLogin)
        except: 
            return Response({"massage":"user không tồn tại"},status=204)
        return Response(historyUserLoginJson.data,status=200)
class HistoryByChapterIDAndUserLogin(APIView):    
    @method_decorator(RoleRequest(allowedRoles=['Admin','NormalUser']))
    def get(self,request,ChapterID):
        try:
            historyUserLoginChapter = History.objects.get(User__pk=request.userID,Chapter__pk=ChapterID)
            historyUserLoginChapterSerializer=HistorySerializer(historyUserLoginChapter)
            return Response(historyUserLoginChapterSerializer.data,status=200)
        except: 
            return Response({"massage":"user này chưa xem Chapter này"},status=204)
    @method_decorator(RoleRequest(allowedRoles=['Admin','NormalUser']))
    def post(self,request,ChapterID):
        try:
            historyUserLoginChapter = History.objects.get(User__pk=request.userID,Chapter__pk=ChapterID)
            historyUserLoginChapterSerializer=HistorySerializer(historyUserLoginChapter)
            return Response(historyUserLoginChapterSerializer.data,status=200)
        except: 
            userLogin = User.objects.get(pk=request.userID)
            chapter = Chapter.objects.get(pk=ChapterID)
            historyUserLoginChapter = History(User=userLogin,Chapter=chapter,HistoryView=datetime.now(),WatchedTime=0)
            historyUserLoginChapter.save()
            historyUserLoginChapterSerializer = HistorySerializer(historyUserLoginChapter)
            return Response(historyUserLoginChapterSerializer.data,status=200)
    def patch(self,request,ChapterID):
        try:
            historyUserLoginChapter = History.objects.get(User__pk=request.userID,Chapter__pk=ChapterID)
        except: 
           
            return Response({"massage":"User không tồn tại"},status=400)
        if  'WatchedTime' in request.data:
            historyUserLoginChapter.WatchedTime=request.data['WatchedTime']
        if   'Rate' in request.data:
            Rate=request.data['Rate']
            historyUserLoginChapter.Rate=Rate
        historyUserLoginChapter.HistoryView=datetime.now()
        historyUserLoginChapter.save()
        
        historyUserLoginChapterSerializer=HistorySerializer(historyUserLoginChapter)
        
        
        return Response(historyUserLoginChapterSerializer.data, status=200)

        
        
