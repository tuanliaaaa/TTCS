from audioop import reverse
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response
from django.http.response import HttpResponseRedirect
def RoleRequest(allowedRoles=[]):
    def decorator(ViewFuntion):
        def wrap(request,*args,**kwargs):
            checkAuthorization = False
            if(len(allowedRoles)==0):checkAuthorization =True
            for allowedRole in allowedRoles:
                try:
                    if allowedRole in request.roles:
                        checkAuthorization = True
                        return ViewFuntion(request,*args,**kwargs)
                except:
                    return Response({"message":"bạn không có quyền truy cập"},status=status.HTTP_403_FORBIDDEN)
            if not checkAuthorization:
                return Response({"message":"bạn không có quyền truy cập"},status=status.HTTP_403_FORBIDDEN)
        return wrap
    return decorator