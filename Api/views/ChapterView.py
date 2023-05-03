from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from Entity.models.Film import Film
from Entity.models.User import User
from Entity.models.History import History
from Entity.models.Category import Category
from Entity.models.Chapter import Chapter
from Entity.models.ActorChapter import ActorChapter
from Entity.models.Actor import Actor
from Serializer.FilmSerializer import FilmSerializer
from Serializer.ChapterSerializer import ChapterSerializer
import numpy as np
import pandas as pd
from core.settings import MEDIA_ROOT,BASE_DIR
import os
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models import Avg

from core.roleLoginDecorater import RoleRequest
from django.utils.decorators import method_decorator
class ChapterHot(APIView):
    @method_decorator(RoleRequest(allowedRoles=['Admin','NormalUser']))
    def get(self,request):
        chapterHotCount = History.objects.values('Chapter__id').annotate(count=Count('id')).order_by('-count')
        try:
            chapter = Chapter.objects.get(pk=chapterHotCount[0]['Chapter__id'])
            chapterSerializer =ChapterSerializer(chapter)
            return Response(chapterSerializer.data,status=200)
        except:
            return Response("[]",status=200)
class FilmChapterID(APIView):
    @method_decorator(RoleRequest(allowedRoles=['Admin','NormalUser']))
    def get(self,request,ChapterID):
        film= Film.objects.get(chapters__pk=ChapterID)
        filmSerializer = FilmSerializer(film)
        return Response(filmSerializer.data,status=200)
class ChapterByID(APIView):
    @method_decorator(RoleRequest(allowedRoles=['Admin']))
    def get(self,request,ChapterID):
        try:
            chapter = Chapter.objects.get(pk=ChapterID) 
            chapterSerializer = ChapterSerializer(chapter)
            return Response(chapterSerializer.data,status=200)
        except:
            return Response({"massage":"Chapter Không tồn tại"},status=400)
    @method_decorator(RoleRequest(allowedRoles=['Admin']))
    def patch(self,request,ChapterID):
        chapter = Chapter.objects.get(pk=ChapterID) 
        actorList= (request.data['ListActor']).split(',')
        if len(request.data['ListActor'])==0:
            return Response({"massage":"Vui lòng nhập Actor"},status=400) 
  
        if request.data['ChapterName']:
            chapter.ChapterName=request.data['ChapterName']

        if request.data['ChapterDescription']:
            chapter.ChapterDescription=request.data['ChapterDescription']
            
        ChapterImage = request.FILES.get('ChapterImage')  
        if ChapterImage:
            image_path = os.path.join(MEDIA_ROOT,'Image',ChapterImage.name)[:-4]+'(0).png'
            check=0
            while  os.path.isfile(image_path) :
                check+=1
                image_path = os.path.join(MEDIA_ROOT,'Image', ChapterImage.name)[:-4]+'('+str(check)+').png'
        
            with open(image_path, 'wb') as f:
                for chunk in ChapterImage.chunks():
                    f.write(chunk)
            ChapterImage=image_path[len(os.path.join(BASE_DIR)):] 
           
            chapter.ChapterImage=ChapterImage
        
        TrailerChapter = request.FILES.get('TrailerChapter')
        if TrailerChapter:
            TrailerChapter_path = os.path.join(MEDIA_ROOT,'Video',TrailerChapter.name)[:-4]+'(0).mp4'
            check=0
            while  os.path.isfile(TrailerChapter_path) :
                check+=1
                TrailerChapter_path = os.path.join(MEDIA_ROOT,'Video', TrailerChapter.name)[:-4]+'('+str(check)+').mp4'
        
            with open(TrailerChapter_path, 'wb') as f:
                for chunk in TrailerChapter.chunks():
                    f.write(chunk)
            TrailerChapter=TrailerChapter_path[len(os.path.join(BASE_DIR)):] 
            chapter.TrailerChapter=TrailerChapter
        Video = request.FILES.get('Video')
        if not request.FILES.get('Video'):
            chapter.ChapterStatus='Đang Ra'
        if Video:
            Video_path = os.path.join(MEDIA_ROOT,'Video',Video.name)[:-4]+'(0).mp4'
            check=0
            while  os.path.isfile(Video_path) :
                check+=1
                Video_path = os.path.join(MEDIA_ROOT,'Video', Video.name)[:-4]+'('+str(check)+').mp4'
        
            with open(Video_path, 'wb') as f:
                for chunk in Video.chunks():
                    f.write(chunk)
            Video=Video_path [len(os.path.join(BASE_DIR)):]
            chapter.Video=Video
            chapter.ChapterStatus="Đã Ra"
            chapter.ChapterPremieredDay= datetime.now()
        chapter.save()
  
        actorsNow = ActorChapter.objects.filter(Chapter=chapter)
        
        for actor in actorList:
            if actor not in [ actorNow.pk for actorNow in actorsNow]:
                actorGet =Actor.objects.get(pk=actor)
                actorChapternew=ActorChapter(Actor=actorGet,Chapter=chapter)
                actorChapternew.save() 
        for actorNow in actorsNow:
            if actorNow.pk in actorList:
                pass
            else:
                actorNow.delete()
        chapterSerializer =ChapterSerializer(chapter)
        return Response(chapterSerializer.data,status=200)
    @method_decorator(RoleRequest(allowedRoles=['Admin']))
    def delete(self,request,ChapterID):
        chapter = Chapter.objects.get(pk=ChapterID)
        chapter.delete()
        return Response({"message":"Xóa thành công"},status=204)

class RecommendView(APIView):
    @method_decorator(RoleRequest(allowedRoles=['Admin','NormalUser']))
    def get(self, request):
        
        history= History.objects.filter(User__id=request.userID)
        #nếu User mới thì recommend cho user chapter hot trong tuần
        if(len(history)==0) :
            chaptersHotCount = History.objects.values('Chapter__id').annotate(count=Count('id'),avg=Avg('Rate')).order_by('-avg','-count').filter(HistoryView__gte=datetime.now()-timedelta(days=7),HistoryView__lt=datetime.now())
            try:
                chapterHotList=[]
                for chapterHotCount in chaptersHotCount:
                    chapterHot = Chapter.objects.get(pk=chapterHotCount['Chapter__id'])
                    chapterHotList.append(chapterHot)
                chapterHotListSerializer =ChapterSerializer(chapterHotList,many=True)
                return Response(chapterHotListSerializer.data,status=200)
            except:
                
                return Response([],status=200)
        #----------------------- Content Based System Recommend -----------------------------
        
        
        #khởi tạo lượt xem của người dùng với thể loại
        categoryUserView=[]
        for i in history:
            for j in i.Chapter.Film.filmcategory.all():
                categoryUserView.append(j.Category.id)
        #khởi tạo lượt xem của người dùng với diễn viên
        actorUserView=[]
        for i in history:
            for j in i.Chapter.chapteractor.all():
                actorUserView.append(j.Actor.id)
        
        #láy toàn bộ chapter User chưa xem 
        chapterAll = Chapter.objects.exclude(id__in=history.values_list('Chapter', flat=True))
        #lấy toàn bộ Thể loại
        categoryAll = Category.objects.all()

        #lấy toàn bộ diễn viên
        actorAll =Actor.objects.all()
        #khởi tạo ma trận với hàng là các chapter người dùng chưa xem còn cột là category,actor
        chapter_matrix = np.zeros((len(chapterAll), len(categoryAll)+len(actorAll)))
        # khởi tạo phần category cho chapter_matrix
        for i in range(len(chapterAll)):
            for j in range(len(categoryAll)):
                if categoryAll[j] in [ i.Category for i in chapterAll[i].Film.filmcategory.all()]:
                    chapter_matrix[i,j]=1
        # khởi tạo phần actor cho chapter_matrix
        for i in range(len(chapterAll)):
            for j in range(len(actorAll)):
                if actorAll[j] in [ i.Actor for i in chapterAll[i].chapteractor.all()]:
                    chapter_matrix[i,j]=1
        print(chapter_matrix)
    
        #khởi tạo ma trận với hàng là User đang đăng nhập(1 hàng) còn cột là category,actor
        userLogin_matrix = []
        # khởi tạo phần category cho userLogin_matrix
        for i in categoryAll:
            if i.id in categoryUserView:
                userLogin_matrix.append(categoryUserView.count(i.id)/len(categoryUserView))
            else:
                userLogin_matrix.append(0)
        # khởi tạo phần actor cho userLogin_matrix
        for i in actorAll:
            if i.id in actorUserView:
                userLogin_matrix.append(actorUserView.count(i.id)/len(actorUserView))
            else:
                userLogin_matrix.append(0)
        print(userLogin_matrix)
        print()
        similarity_scores = cosine_similarity( np.array(userLogin_matrix).reshape(1,-1),chapter_matrix)
        sorted_indices = np.argsort(similarity_scores, axis=1)[0]
        
        # Lấy ra các chapter được recommend
        recommended_chapters = []
        for i in sorted_indices:
            if len(recommended_chapters)>5:
                break
            if chapterAll[int(i)].ChapterStatus =='Đã ra':
                recommended_chapters.append(chapterAll[int(i)])
        #----------------------- Collaborative Filtering System Recommend -----------------------------

        
        # Lấy thông tin người dùng đăng nhập
        userLogin= User.objects.get(pk=request.userID) 
        
        # Lấy toàn bộ người dùng 
        users = User.objects.all()
        # Tìm kiếm vị trí của người dùng
        for i in range(len(users)):
            if users[i].pk==userLogin.pk:
                indexUserLogin=i
                break
            
        # Lấy toàn bộ Chapter
        chapters = Chapter.objects.all()
        
        # Tạo ma trận full 0 với số hàng là số chapter và số cột là số User
        ratings_matrix = np.zeros(( len(chapters),len(users)))
        
        # thay đổi các giá trị 0 thành điểm số Rate trong history nếu người dùng đã đánh giá
        for i, chapter in enumerate(chapters):
            for j, user in enumerate(users):
                # get all ratings for this user and chapter
                try:
                    rating = History.objects.get(User=user, Chapter=chapter)
                    ratings_matrix[i, j] = rating.Rate
                except:
                    pass
        print(ratings_matrix)
        # chuẩn hóa ma trận để giảm các rating giống nhau thể hiện rõ hơn sự đánh giá trái triều:
        ratings_matrixx = np.zeros(( len(chapters),len(users)))
        
        for i in range(len(ratings_matrix)):
            fullZero=False
            try:
                avg=np.sum(ratings_matrix[i])/np.count_nonzero(ratings_matrix[i])   
            except:fullZero=True
            if not fullZero:
                for j in range(len(ratings_matrixx[i])):
                    if(ratings_matrix[i,j]!=0):
                        ratings_matrixx[i,j]=  ratings_matrix[i,j]-avg
        print(ratings_matrixx)
        # Hoàn Thành ma trận rating của UserLogin với chapter
        ratingChapterUser=[]
        for i in range(len(ratings_matrix)):
            if(ratings_matrix[i][indexUserLogin]!=0):
                ratingChapterUser.append(ratings_matrix[i][indexUserLogin])
            else:
                ratingList=[]
                for j in range(len(ratings_matrixx)):
                        newChapter1=[]
                        newChapter2=[]
                        # Dùng vòng for và loại bỏ các giá trị =0 của cả 2 vecto để bỏ đi các rating =0
                        for l in range(len(ratings_matrixx)):
                            if ratings_matrixx[i][l] !=0 and ratings_matrixx[j][l]!=0:
                                newChapter1.append(ratings_matrixx[i][l])
                                newChapter2.append(ratings_matrixx[j][l])
                        # Tính độ tương đồng giữa 2 chapter bằng cosin 
                        cos_sim = np.dot(newChapter1, newChapter2) / (np.linalg.norm(newChapter1) * np.linalg.norm(newChapter2))
                        if   np.isnan(cos_sim):
                            cos_sim=0
                        ratingList.append(cos_sim)
                #lấy ra 2 chapter giông chapter đang tính rating nhất và tính trugn bình có trọng số
                sortRatingList=np.argsort(ratingList)
                ratingChapterUser.append((ratingList[sortRatingList[0]]*ratings_matrix[sortRatingList[0]][indexUserLogin]+ratingList[sortRatingList[1]]*ratings_matrix[sortRatingList[1]][indexUserLogin])/(ratingList[sortRatingList[0]]+ratingList[sortRatingList[1]]))
        sorted_index = sorted(range(len(ratingChapterUser)), key=lambda i: ratingChapterUser[i], reverse=True)    
        print(ratingChapterUser)
        
        # Liệt kê film recomend
        for i in sorted_index:
            checkExit=False
            checkViewed=False
            for j in recommended_chapters:
                if chapters[i].pk==j.pk:
                    checkExit=True
                    break
            for j in chapterAll:
                if chapters[i].pk==j.pk:
                    checkViewed=True
            if checkExit or not checkViewed:continue     
            if len(recommended_chapters)>10:
                break
            if chapters[i].ChapterStatus =='Đã ra' :
                
                 
                recommended_chapters.append(chapters[i])
        chapterRecommendSerializer= ChapterSerializer(recommended_chapters,many=True)
        return Response(chapterRecommendSerializer.data,status=200)
        
class ChapterHotFromDaytoDay(APIView):
    def get(self,request):
        if request.GET.get('fromDay'):
            fromDay = datetime.strptime(request.GET.get('fromDay'), "%Y-%m-%d")
        else:
            fromDay=datetime.strptime('22/12/1945', "%d/%m/%Y")
        if request.GET.get('toDay'):
            toDay = datetime.strptime(request.GET.get('toDay'), "%Y-%m-%d")+timedelta(days=1)
        else:      
            toDay =  datetime.now()

        chaptersHotCount = History.objects.values('Chapter__id').annotate(count=Count('id'),avg=Avg('Rate')).order_by('-count').filter(HistoryView__gte=fromDay,HistoryView__lt=toDay)
        try:
            chapterHotList=[]
            for chapterHotCount in chaptersHotCount:
                chapterHot = Chapter.objects.get(pk=chapterHotCount['Chapter__id'])
                
                chapterHotList.append({"id":chapterHot.id,"RateAvg":chapterHotCount['avg'],"CountView":chapterHotCount['count'],"ChapterImage":chapterHot.ChapterImage,"ChapterName":chapterHot.ChapterName})
                
            return Response(chapterHotList,status=200)
        except:
            return Response("[]",status=200)