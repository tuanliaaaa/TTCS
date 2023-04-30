from Entity.models.Category import Category
from rest_framework.views import APIView
from rest_framework.response import Response
from Serializer.CategorySerializer import CategorySerializer
from Serializer.CategoryFilmSerializer import CategoryFilmsSerializer
from django.db.models import Q
from core.roleLoginDecorater import RoleRequest
from django.utils.decorators import method_decorator
class AllCategory(APIView):
    @method_decorator(RoleRequest(allowedRoles=['Admin','NormalUser']))
    def get(self,request):
        page = request.GET.get('page',1)
        per_page = request.GET.get('per_page', 2) 
        offSet = (int(page) - 1) * int(per_page)
        limit = offSet + int(per_page)
        categoryList = Category.objects.all()[offSet:limit]
        categoryListSerializer = CategorySerializer(categoryList,many=True)
        return Response(categoryListSerializer.data,status=200)
    @method_decorator(RoleRequest(allowedRoles=['Admin']))
    def post(self,request):          
        categorySerializer = CategorySerializer(data=request.data)
        if categorySerializer.is_valid():
            categorySerializer.save()
            return Response(categorySerializer.data, status=201)
        return Response(categorySerializer.errors, status=400)
class CategoryById(APIView):
    @method_decorator(RoleRequest(allowedRoles=['Admin','NormalUser']))
    def get(self,request,CategoryID):
        try:
            category = Category.objects.get(pk=CategoryID)
            CategorySerializer = CategoryFilmsSerializer(category)
            return Response(CategorySerializer.data,status=200)
        except:
            return Response({"massage":"Category không tồn tại"},status=204)
    @method_decorator(RoleRequest(allowedRoles=['Admin']))
    def patch(self,request,CategoryID):
        try:
            category= Category.objects.get(pk=CategoryID)
            categoryUpdateSerializer = CategorySerializer(category, data=request.data,partial=True)
            if categoryUpdateSerializer.is_valid():
                categoryUpdateSerializer.save()
                return Response(categoryUpdateSerializer.data)
            return Response(categoryUpdateSerializer.errors, status=400)
        except:
            return Response({"massage":"Category không tồn tại"},status=200)
    @method_decorator(RoleRequest(allowedRoles=['Admin']))
    def delete(self,request,CategoryID):
        try:
            category= Category.objects.get(pk=CategoryID)
            category.delete()
            return Response({'massage':'User đã xóa thành công'},status=204)
        except:
            return Response({"massage":"User không tồn tại"},status=200)
class SearchCategory(APIView):
    @method_decorator(RoleRequest(allowedRoles=['Admin','NormalUser']))
    def get(self,request,Categoryname):
        page = request.GET.get('page',1)
        per_page = request.GET.get('per_page', 2) 
        offSet = (int(page) - 1) * int(per_page)
        limit = offSet + int(per_page)
        category= Category.objects.filter(Q(CategoryName__icontains=Categoryname)).distinct()[offSet:limit]
        categorySerializer = CategorySerializer(category,many=True)
        return Response(categorySerializer.data,status=200)
class CategoryGetAll(APIView):
    @method_decorator(RoleRequest(allowedRoles=['Admin','NormalUser']))
    def get(self,request):
        category= Category.objects.all()
        categorySerializer = CategorySerializer(category,many=True)
        return Response(categorySerializer.data,status=200)

   