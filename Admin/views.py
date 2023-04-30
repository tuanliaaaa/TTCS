from django.shortcuts import render
from django.views import View
# Create your views here.
class AdminLogin(View):
    def get(self,request):
        return render(request,'AdminLogin.html')
class UserManage(View):
    def get(self,request):
        return render(request,'UserManage.html')
class EditUser(View):
    def get(self,request,UserID):
        return render(request,'EditUser.html')
class CategoryManage(View):
    def get(self,request):
        return render(request,'CategoryManage.html')
class EditCategory(View):
    def get(self,request,CategoryID):
        return render(request,'EditCategory.html')
class AddCategory(View):
    def get(self,request):
        return render(request,'AddCategory.html')
class FilmManage(View):
    def get(self,request):
        return render(request,'FilmManage.html')
class EditFilm(View):
    def get(self,request,FilmID):
        return render(request,'EditFilm.html')
class AddFilm(View):
    def get(self,request):
        return render(request,'AddFilm.html')
class AddChapterByFilmID(View):
    def get(self,request,FilmID):
        return render(request,'AddChapterFilm.html')
class ActorManage(View):
    def get(self,request):
        return render(request,'ActorManage.html')
class AddActor(View):
    def get(self,request):
        return render(request,'AddActor.html')
class EditActor(View):
    def get(self,request,ActorID):
        return render(request,'EditActor.html')
class EditChapter(View):
    def get(self,request,ChapterID):
        return render(request,'EditChapterFilm.html')