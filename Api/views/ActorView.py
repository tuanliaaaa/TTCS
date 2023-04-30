from Entity.models.Actor import Actor
from rest_framework.views import APIView
from rest_framework.response import Response
from Serializer.ActorSerializer import ActorSerializer
from Serializer.ActorChapterSerializer import ActorChaptersSerializer
from django.db.models import Q
from core.roleLoginDecorater import RoleRequest
from django.utils.decorators import method_decorator
class AllActor(APIView):
    @method_decorator(RoleRequest(allowedRoles=['Admin','NormalUser']))
    def get(self,request):
        page = request.GET.get('page',1)
        per_page = request.GET.get('per_page', 2) 
        offSet = (int(page) - 1) * int(per_page)
        limit = offSet + int(per_page)
        actorList = Actor.objects.all()[offSet:limit]
        actorListSerializer = ActorSerializer(actorList,many=True)
        return Response(actorListSerializer.data,status=200)
    @method_decorator(RoleRequest(allowedRoles=['Admin']))
    def post(self,request):          
        actorSerializer = ActorSerializer(data=request.data)
        if actorSerializer.is_valid():
            actorSerializer.save()
            return Response(actorSerializer.data, status=201)
        return Response(actorSerializer.errors, status=400)
class ActorById(APIView):
    @method_decorator(RoleRequest(allowedRoles=['Admin','NormalUser']))
    def get(self,request,ActorID):
        try:
            actor = Actor.objects.get(pk=ActorID)
            
            ActorSerializer = ActorChaptersSerializer(actor)
            return Response(ActorSerializer.data,status=200)
        except:
            return Response({"massage":"Actor không tồn tại"},status=204)
    @method_decorator(RoleRequest(allowedRoles=['Admin']))
    def patch(self,request,ActorID):
        try:
            actor= Actor.objects.get(pk=ActorID)
            actorUpdateSerializer = ActorSerializer(actor, data=request.data,partial=True)
            if actorUpdateSerializer.is_valid():
                actorUpdateSerializer.save()
                return Response(actorUpdateSerializer.data)
            return Response(actorUpdateSerializer.errors, status=400)
        except:
            return Response({"massage":"Actor không tồn tại"},status=200)
    @method_decorator(RoleRequest(allowedRoles=['Admin']))
    def delete(self,request,ActorID):
        try:
            actor= Actor.objects.get(pk=ActorID)
            actor.delete()
            return Response({'massage':'User đã xóa thành công'},status=204)
        except:
            return Response({"massage":"User không tồn tại"},status=200)
class SearchActor(APIView):
    @method_decorator(RoleRequest(allowedRoles=['Admin','NormalUser']))
    def get(self,request,Actorname):
        page = request.GET.get('page',1)
        per_page = request.GET.get('per_page', 2) 
        offSet = (int(page) - 1) * int(per_page)
        limit = offSet + int(per_page)
        actor= Actor.objects.filter(Q(ActorName__icontains=Actorname)).distinct()[offSet:limit]
        actorSerializer = ActorSerializer(actor,many=True)
        return Response(actorSerializer.data,status=200)
class ActorGetAll(APIView):
    @method_decorator(RoleRequest(allowedRoles=['Admin','NormalUser']))
    def get(self,request):
        actor= Actor.objects.all()
        actorSerializer = ActorSerializer(actor,many=True)
        return Response(actorSerializer.data,status=200)
