from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from Entity.models.Category import Category
from Serializer.CategoryFilmSerializer import CategoryFilmsSerializer
from core.roleLoginDecorater import RoleRequest
from django.utils.decorators import method_decorator
class CategoryAllFilm(APIView):
    @method_decorator(RoleRequest(allowedRoles=['Admin','NormalUser']))
    def get(self,request):
        categoryFilm = Category.objects.all()
        categoryFilmSerializer =CategoryFilmsSerializer(categoryFilm,many=True)
        return Response(categoryFilmSerializer.data)