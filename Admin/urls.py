from django.urls import path
from .views import AdminLogin,UserManage,EditUser,CategoryManage,EditCategory,AddCategory,FilmManage,EditFilm,AddFilm,AddChapterByFilmID,ActorManage,AddActor,EditActor,EditChapter,DashBoard
urlpatterns = [
    path('Login', AdminLogin.as_view()),
    path('User', UserManage.as_view()),
    path('Category', CategoryManage.as_view()),
    path('Film', FilmManage.as_view()),
    path('Actor', ActorManage.as_view()),
    path('AddCategory', AddCategory.as_view()),
    path('AddFilm', AddFilm.as_view()),
    path('AddActor', AddActor.as_view()),
    path('AddChapterByFilmID/<int:FilmID>', AddChapterByFilmID.as_view()),
    path('EditUser/<int:UserID>',EditUser.as_view()),
    path('EditCategory/<int:CategoryID>',EditCategory.as_view()),
    path('EditFilm/<int:FilmID>',EditFilm.as_view()),
    path('EditActor/<int:ActorID>',EditActor.as_view()),
    path('EditChapter/<int:ChapterID>',EditChapter.as_view()),
    path('Home',DashBoard.as_view())
    
]