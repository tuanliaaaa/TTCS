from django.urls import path
from .views.token import Token
from .views.ChapterView import ChapterHot,FilmChapterID,RecommendView,ChapterByID
from .views.UserView import Signup,AllUser,UserById,SearchUser,UserByIdForAdmin,UserByLogin,ChangePassword
from .views.CategoryFilmView import CategoryAllFilm
from .views.FilmViews import FilmSearch,AllFilm,FilmByID,ChapterByFilmID
from .views.HistoryView import HistoryUserLogin,HistoryByChapterIDAndUserLogin
from .views.CategoryView import CategoryById,AllCategory,SearchCategory,CategoryGetAll
from .views.ActorView import AllActor,ActorById,SearchActor,ActorGetAll
urlpatterns = [
    path('Token',Token.as_view()),
    path('Signup',Signup.as_view()),
    path('ChapterHot',ChapterHot.as_view()),
    path('CategoryAllFim',CategoryAllFilm.as_view()),
    path('FilmChapterIDChapterID/<int:ChapterID>',FilmChapterID.as_view()),
    path('HistoryUserLogin',HistoryUserLogin.as_view()),
    path('HistoryByChapterIDAndUserLogin/<int:ChapterID>',HistoryByChapterIDAndUserLogin.as_view()),
    path('FindFilm/<str:filmSearch>',FilmSearch.as_view()),
    path('AllUser',AllUser.as_view()),
    path('UserByID/<int:UserID>',UserById.as_view()),
    path('UserByLogin',UserByLogin.as_view()),
    path('UserByIDForAdmin/<int:UserID>',UserByIdForAdmin.as_view()),
    path('UserByName/<str:Username>',SearchUser.as_view()),
    path('ChangePassword',ChangePassword.as_view()),
    path('AllCategory',AllCategory.as_view()),
    path('AllgetCategory',CategoryGetAll.as_view()),
    path('CategoryById/<int:CategoryID>',CategoryById.as_view()),
    path('CategoryByName/<str:Categoryname>',SearchCategory.as_view()),
    path('AllFilm',AllFilm.as_view()),
    path('FilmByID/<int:FilmID>',FilmByID.as_view()),
    path('ChapterByFilmID/<int:FilmID>',ChapterByFilmID.as_view()),
    path('Recommend',RecommendView.as_view()),
    path("ChapterByID/<int:ChapterID>", ChapterByID.as_view()),
    path('ActorByID/<int:ActorID>',ActorById.as_view()),
    path('AllActor',AllActor.as_view()),
    path('AllgetActor',ActorGetAll.as_view()),
    path('ActorByName/<str:Actorname>',SearchActor.as_view()),
]