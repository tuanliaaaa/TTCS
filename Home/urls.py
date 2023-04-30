from django.urls import path
from .views import Home,Login,Signup,DetailVideo,image_view,video_view,UserInfor,UserChangePassword
urlpatterns = [
    path('Home', Home.as_view()),
    path('Login',Login.as_view()),
    path('Signup',Signup.as_view()),
    path('DetailVideo/<int:IDChapter>',DetailVideo.as_view()),
    path('Home/Media/Image/<str:image_name>',image_view),
    path('Home/Media/Video/<str:video_name>',video_view),
    path('Home/UserInfor',UserInfor.as_view()),
    path('Home/UserChangePassword',UserChangePassword.as_view()),
]
