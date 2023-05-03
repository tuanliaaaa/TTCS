from Entity.models.Film import Film
from Entity.models.Category import Category
from Entity.models.Chapter import Chapter
from Entity.models.CategoryFilm import CategoryFilm
from Entity.models.Actor import Actor
from Entity.models.ActorChapter import ActorChapter
from Serializer.ChapterSerializer import ChapterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from core.settings import MEDIA_ROOT,BASE_DIR
import os
from datetime import datetime
import json
from core.roleLoginDecorater import RoleRequest
from django.utils.decorators import method_decorator
from Serializer.FilmSerializer import FilmSerializer
from Serializer.CategoryFilmSerializer import FilmCategorysSerializer
class FilmSearch(APIView):
    @method_decorator(RoleRequest(allowedRoles=['Admin','NormalUser']))
    def get(self,request,filmSearch):
        film = Film.objects.filter(Q(FilmName__icontains=filmSearch)|Q(chapters__ChapterName__icontains=filmSearch)|Q(chapters__ChapterDescription__icontains=filmSearch)).distinct()
        filmserializer = FilmSerializer(film,many=True)
        return Response(filmserializer.data,status=200)
class AllFilm(APIView):
    @method_decorator(RoleRequest(allowedRoles=['Admin','NormalUser']))
    def get(self,request):
        page = request.GET.get('page',1)
        per_page = request.GET.get('per_page', 2) 
        offSet = (int(page) - 1) * int(per_page)
        limit = offSet + int(per_page)
        filmList = Film.objects.all()[offSet:limit]
        filmListSerializer = FilmSerializer(filmList,many=True)
        return Response(filmListSerializer.data,status=200)
    @method_decorator(RoleRequest(allowedRoles=['Admin']))
    def post(self,request):       
        if not request.FILES.get('Image'):
            return Response({"massage":"Vui lòng nhập Image"},status=400)    
        if not request.FILES.get('BannerFilmName'):
            return Response({"massage":"Vui lòng nhập BannerFilmName"},status=400)  
        if not request.FILES.get('TrailerFilm'):
            return Response({"massage":"Vui lòng nhập TrailerFilm"},status=400)  
        if not request.FILES.get('Video'):
            status="Đang ra"
        else:
            status="Đã ra"
        if(request.data['FilmBollen']=='1'):
            FilmBollen=1
            if not request.data['ChapterName']:
                return Response({"massage":"Vui lòng nhập ChapterName"},status=400)  
            if not request.data['ChapterDescription']:
                return Response({"massage":"Vui lòng nhập ChapterDescription"},status=400)  
        else:
            FilmBollen=0
        categoryList= (request.data['ListCategory']).split(',')
        if len(request.data['ListCategory'])==0:
            return Response({"massage":"Vui lòng nhập Category"},status=400)  
        actorList= (request.data['ListActor']).split(',')
        if len(request.data['ListActor'])==0:
            return Response({"massage":"Vui lòng nhập Actor"},status=400)  
        if not request.data['FilmName']:
            return Response({"massage":"Vui lòng nhập FilmName"},status=400)  
        if not request.data['Description']:
            return Response({"massage":"Vui lòng nhập Description"},status=400)  
        Image = request.FILES.get('Image')     
        
        if Image:
            image_path = os.path.join(MEDIA_ROOT,'Image',Image.name)[:-4]+'(0).png'
            check=0
            while  os.path.isfile(image_path) :
                check+=1
                image_path = os.path.join(MEDIA_ROOT,'Image', Image.name)[:-4]+'('+str(check)+').png'
        
            with open(image_path, 'wb') as f:
                for chunk in Image.chunks():
                    f.write(chunk)
            Image=image_path[len(os.path.join(BASE_DIR)):] 
        else:
            Image=''
        BannerFilmName = request.FILES.get('BannerFilmName')
        if BannerFilmName:
            BannerFilmName_path = os.path.join(MEDIA_ROOT,'Image',BannerFilmName.name)[:-4]+'(0).png'
            check=0
            while  os.path.isfile(BannerFilmName_path) :
                check+=1
                BannerFilmName_path = os.path.join(MEDIA_ROOT,'Image', BannerFilmName.name)[:-4]+'('+str(check)+').png'
        
            with open(BannerFilmName_path, 'wb') as f:
                for chunk in BannerFilmName.chunks():
                    f.write(chunk)
            BannerFilmName=BannerFilmName_path [len(os.path.join(BASE_DIR)):]
        else:
            BannerFilmName=''
        TrailerFilm = request.FILES.get('TrailerFilm')
        if TrailerFilm:
            TrailerFilm_path = os.path.join(MEDIA_ROOT,'Video',TrailerFilm.name)[:-4]+'(0).mp4'
            check=0
            while  os.path.isfile(TrailerFilm_path) :
                check+=1
                TrailerFilm_path = os.path.join(MEDIA_ROOT,'Video', TrailerFilm.name)[:-4]+'('+str(check)+').mp4'
        
            with open(TrailerFilm_path, 'wb') as f:
                for chunk in TrailerFilm.chunks():
                    f.write(chunk)
            TrailerFilm=TrailerFilm_path[len(os.path.join(BASE_DIR)):] 
        else:
            TrailerFilm=''
        Video = request.FILES.get('Video')
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
        else:
            Video=''    
        film=Film(FilmName=request.data['FilmName'],FilmDescription=request.data['Description'],BannerFilmName=BannerFilmName,FilmImage=Image,TrailerFilm=TrailerFilm,FilmBollen=FilmBollen)
        film.save()
        for category in categoryList:
            category = Category.objects.get(pk=category)
            categoryFilm = CategoryFilm(Category=category,Film=film)
            categoryFilm.save() 
        
        if(FilmBollen==0):
            chapter=Chapter(ChapterName=request.data['FilmName'],ChapterDescription=request.data['Description'],Video=Video,ChapterImage=Image,TrailerChapter=TrailerFilm,Film=film,ChapterStatus=status)
            chapter.save()
        else:
            chapter=Chapter(ChapterName=request.data['ChapterName'],ChapterDescription=request.data['ChapterDescription'],Video=Video,ChapterImage=Image,TrailerChapter=TrailerFilm,Film=film,ChapterStatus=status)
            chapter.save()
        for actor in actorList:
            actor = Actor.objects.get(pk=actor)
            actorChapter = ActorChapter(Actor=actor,Chapter=chapter)
            actorChapter.save() 
        filmSerializer =FilmSerializer(film)
        return Response(filmSerializer.data, status=201)
class FilmByID(APIView):
    @method_decorator(RoleRequest(allowedRoles=['Admin','NormalUser']))
    def get(self,request,FilmID):
        try:
            film = Film.objects.get(pk=FilmID)
            FilmSerializer = FilmCategorysSerializer(film)
            return Response(FilmSerializer.data,status=200)
        except:
            return Response({"massage":"Film không tồn tại"},status=204)
    @method_decorator(RoleRequest(allowedRoles=['Admin']))
    def patch(self,request,FilmID):
        try:
            film= Film.objects.get(pk=FilmID)
            chapter = Chapter.objects.filter(Film=film,ChapterNumber=1)[0]
            
            if(request.data['FilmBollen']=='1' and film.FilmBollen==0):
                FilmBollen=1
                if not request.data['ChapterName']:
                    return Response({"massage":"Vui lòng nhập ChapterName"},status=400)  
                if not request.data['ChapterDescription']:
                    return Response({"massage":"Vui lòng nhập ChapterDescription"},status=400)  
            else:
                if request.data['FilmBollen']=='0' and film.FilmBollen==1:
                    return Response({"massage":"Không thể đổi type Film"},status=400) 
                FilmBollen=0
            categoryList= (request.data['ListCategory']).split(',')
            if len(request.data['ListCategory'])==0:
                return Response({"massage":"Vui lòng nhập Category"},status=400)  
            actorList= (request.data['ListActor']).split(',')
            if len(request.data['ListActor'])==0:
                return Response({"massage":"Vui lòng nhập Actor"},status=400) 
            
            Image = request.FILES.get('Image')     
            if Image:
                image_path = os.path.join(MEDIA_ROOT,'Image',Image.name)[:-4]+'(0).png'
                check=0
                while  os.path.isfile(image_path) :
                    check+=1
                    image_path = os.path.join(MEDIA_ROOT,'Image', Image.name)[:-4]+'('+str(check)+').png'
            
                with open(image_path, 'wb') as f:
                    for chunk in Image.chunks():
                        f.write(chunk)
                Image=image_path[len(os.path.join(BASE_DIR)):] 
                film.FilmImage=Image
            
            BannerFilmName = request.FILES.get('BannerFilmName')
            if BannerFilmName:
                BannerFilmName_path = os.path.join(MEDIA_ROOT,'Image',BannerFilmName.name)[:-4]+'(0).png'
                check=0
                while  os.path.isfile(BannerFilmName_path) :
                    check+=1
                    BannerFilmName_path = os.path.join(MEDIA_ROOT,'Image', BannerFilmName.name)[:-4]+'('+str(check)+').png'
            
                with open(BannerFilmName_path, 'wb') as f:
                    for chunk in BannerFilmName.chunks():
                        f.write(chunk)
                BannerFilmName=BannerFilmName_path [len(os.path.join(BASE_DIR)):]
                film.BannerFilmName=BannerFilmName
            TrailerFilm = request.FILES.get('TrailerFilm')
            if TrailerFilm:
                TrailerFilm_path = os.path.join(MEDIA_ROOT,'Video',TrailerFilm.name)[:-4]+'(0).mp4'
                check=0
                while  os.path.isfile(TrailerFilm_path) :
                    check+=1
                    TrailerFilm_path = os.path.join(MEDIA_ROOT,'Video', TrailerFilm.name)[:-4]+'('+str(check)+').mp4'
            
                with open(TrailerFilm_path, 'wb') as f:
                    for chunk in TrailerFilm.chunks():
                        f.write(chunk)
                TrailerFilm=TrailerFilm_path[len(os.path.join(BASE_DIR)):] 
                film.TrailerFilm=TrailerFilm
            Video = request.FILES.get('Video')
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
            
            if request.data['FilmName']:
                film.FilmName=request.data['FilmName']
            if request.data['Description']:
                film.FilmDescription=request.data['Description']

            if FilmBollen != film.FilmBollen:
                film.FilmBollen= FilmBollen
                
                chapter.ChapterName=request.data['ChapterName']
                chapter.ChapterDescription= request.data['ChapterDescription'] 
            chapter.save()
            film.save()
            categorysNow = CategoryFilm.objects.filter(Film=film)
            for category in categoryList:
                if category not in [ categoryNow.pk for categoryNow in categorysNow]:
                    categoryGet =Category.objects.get(pk=category)
                    categoryFilmnew=CategoryFilm(Category=categoryGet,Film=film)
                    categoryFilmnew.save() 
            for categoryNow in categorysNow:
                if categoryNow.pk in categoryList:
                    pass
                else:
                    categoryNow.delete()
            
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
            filmSerializer =FilmSerializer(film)
            return Response(filmSerializer.data, status=200)
        except:
            return Response({"massage":"Category không tồn tại"},status=204)
    @method_decorator(RoleRequest(allowedRoles=['Admin']))
    def delete(self,request,FilmID):
        try:
            film= Film.objects.get(pk=FilmID)
            film.delete()
            return Response({'massage':'Film đã xóa thành công'},status=204)
        except:
            return Response({"massage":"Film không tồn tại"},status=200)
class ChapterByFilmID(APIView):
    @method_decorator(RoleRequest(allowedRoles=['Admin','NormalUser']))
    def get(self,request,FilmID):
        chapter= Chapter.objects.filter(Film__id=FilmID)
        chapterSerializer = ChapterSerializer(chapter,many=True)
        return Response(chapterSerializer.data,status=200)
    @method_decorator(RoleRequest(allowedRoles=['Admin']))
    def post(self,request,FilmID):
        film = Film.objects.get(pk=FilmID)
        if not request.FILES.get('ChapterImage'):
            return Response({"massage":"Vui lòng nhập ChapterImage"},status=400)    
        if not request.FILES.get('TrailerChapter'):
            return Response({"massage":"Vui lòng nhập TrailerChapter"},status=400)  
        if not request.data['ChapterName']:
            return Response({"massage":"Vui lòng nhập ChapterName"},status=400)
        actorList= (request.data['ListActor']).split(',')
        if len(request.data['ListActor'])==0:
            return Response({"massage":"Vui lòng nhập Actor"},status=400)   
        if not request.data['ChapterDescription']:
            return Response({"massage":"Vui lòng nhập ChapterDescription"},status=400)  
        ChapterCreateDay=datetime.now()
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
            
        else:
            ChapterImage=''
        TrailerChapter = request.FILES.get('TrailerChapter')
        if TrailerChapter:
            TrailerChapter_path = os.path.join(MEDIA_ROOT,'Image',TrailerChapter.name)[:-4]+'(0).png'
            check=0
            while  os.path.isfile(TrailerChapter_path) :
                check+=1
                TrailerChapter_path = os.path.join(MEDIA_ROOT,'Image', TrailerChapter.name)[:-4]+'('+str(check)+').png'
        
            with open(TrailerChapter_path, 'wb') as f:
                for chunk in TrailerChapter.chunks():
                    f.write(chunk)
            TrailerChapter=TrailerChapter_path [len(os.path.join(BASE_DIR)):]
        else:
            TrailerChapter=''
        
        Video = request.FILES.get('Video')
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
            Chapterstatus='Đã Ra'
            chapterNew =  Chapter(Film=film,ChapterName=request.data['ChapterName'],ChapterDescription=request.data['ChapterDescription'],TrailerChapter=TrailerChapter,ChapterImage=ChapterImage,Video=Video,ChapterStatus=Chapterstatus,ChapterCreateDay=ChapterCreateDay,ChapterPremieredDay=datetime.now())
        else:
            Chapterstatus='Đang Ra'
            Video=''
            chapterNew =  Chapter(Film=film,ChapterName=request.data['ChapterName'],ChapterDescription=request.data['ChapterDescription'],TrailerChapter=TrailerChapter,ChapterImage=ChapterImage,Video=Video,ChapterStatus=Chapterstatus,ChapterCreateDay=ChapterCreateDay)
        chapterNew.save()
        for actor in actorList:
            actor = Actor.objects.get(pk=actor)
            actorChapter = ActorChapter(Actor=actor,Chapter=chapterNew)
            actorChapter.save() 
        chapterNewSerializer = ChapterSerializer(chapterNew)
        return Response(chapterNewSerializer.data,status=201)
class SearchFilmPage(APIView):
    @method_decorator(RoleRequest(allowedRoles=['Admin']))
    def get(self,request,Filmname):
        page = request.GET.get('page',1)
        per_page = request.GET.get('per_page', 2) 
        offSet = (int(page) - 1) * int(per_page)
        limit = offSet + int(per_page)
        filmList = Film.objects.filter(Q(FilmName__icontains=Filmname)|Q(FilmDescription=Filmname)|Q(chapters__ChapterName=Filmname))[offSet:limit]
        filmListSerializer = FilmSerializer(filmList,many=True)
        return Response(filmListSerializer.data,status=200)

    
