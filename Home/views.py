from django.shortcuts import render
from django.views import View
import os
from django.http import HttpResponse
from core.settings import MEDIA_ROOT
class Home(View):
    def get(self, request):
        return render(request, 'Home.html')
class Login(View):
    def get(self,request):
        return render(request,'Login.html')
class Signup(View):
    def get(self,request):
        return render(request,'Signup.html')
class DetailVideo(View):
    def get(self,request,IDChapter):
        return render(request,'Detail.html')


def image_view(request, image_name):

    image_dir = MEDIA_ROOT
    
    # Tạo đường dẫn tới tệp hình ảnh cần trả về
    image_path = os.path.join(image_dir,"Image", image_name)
    
    # Đọc nội dung của tệp hình ảnh
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # Trả về nội dung của hình ảnh dưới dạng phản hồi HTTP
    response = HttpResponse(content_type='image/*')
    response.write(image_data)
    
    return response
def video_view(request, video_name):
    image_dir = MEDIA_ROOT
    
    # Tạo đường dẫn tới tệp hình ảnh cần trả về
    image_path = os.path.join(image_dir,"Video", video_name)
    
    # Đọc nội dung của tệp hình ảnh
    with open(image_path, 'rb') as f:
    
        response = HttpResponse(f.read(), content_type='video/mp4')
        response['Content-Disposition'] = 'inline; filename=' + video_name
    return response
class UserInfor(View):
    def get(self,request):
        return render(request,'UserInfor.html')
class UserChangePassword(View):
    def get(self,request):
        return render(request,'ChangePassword.html')