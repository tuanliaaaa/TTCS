from rest_framework import status
from rest_framework.response import Response
from Entity.models.User import User
from  core.settings import SECRET_KEY
import jwt
import json
from datetime import datetime,timedelta,timezone
from rest_framework.decorators import APIView
from Entity.models.Role import Role
from Entity.models.UserRole import UserRole
class Token(APIView):
    def post(self,request):
        exp=datetime.now(tz=timezone.utc) + timedelta(minutes=50)
        userRequestToken =request.data     
        if 'Username' not in userRequestToken or not userRequestToken['Username']:
            return Response({"message":"Vui lòng nhập Username"},status=status.HTTP_400_BAD_REQUEST)
        if 'Password' not in userRequestToken or not userRequestToken['Password']:
            return Response({"message":"Vui lòng nhập Password"},status=status.HTTP_400_BAD_REQUEST)
        try:
            user= User.objects.get(UserName=userRequestToken['Username'],Password=userRequestToken['Password'])

        except:    
            return Response({"message":"User này không tồn tại"},status=status.HTTP_404_NOT_FOUND)
        roles=[]
        userRoles=UserRole.objects.filter(User=user)
        for userRole in userRoles:
            roles.append(userRole.Role.RoleName)
        payLoad = {'UserID':user.pk,"Username":user.UserName,"Roles":roles,"exp":exp}
        jwtData = jwt.encode(payLoad,SECRET_KEY,) 
        jwtUser={"access":jwtData}
        return Response(jwtUser,status=status.HTTP_201_CREATED)
        
