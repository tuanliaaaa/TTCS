from  core.settings import SECRET_KEY
import jwt
from rest_framework.response import Response
from rest_framework import status
import json
from django.http.response import HttpResponse
class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):   
        if 'Authorization' in request.headers:
            jwtTokenSplit=request.headers['Authorization'].split(' ')
            jwtTokenPayload = jwtTokenSplit[1]
            try:
                payLoad=jwt.decode(jwtTokenPayload, SECRET_KEY, algorithms=["HS256"])
                request.roles=payLoad['Roles']
                
                request.userID=payLoad['UserID']
                
            except jwt.ExpiredSignatureError:
                return HttpResponse('{"message":"Token đã hết hạn"}',status =status.HTTP_403_FORBIDDEN)
            except:
                return HttpResponse('{"message":"Token Không Hợp Lê"}',status =status.HTTP_403_FORBIDDEN)
        response = self.get_response(request)
        return response