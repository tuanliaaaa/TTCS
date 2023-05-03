from audioop import reverse
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response
from django.http.response import HttpResponseRedirect
# def RoleRequest(allowedRoles=[]):
#     def decorator(ViewFuntion):
#         def wrap(request,*args,**kwargs):
#             checkAuthorization = False
#             if(len(allowedRoles)==0):checkAuthorization =True
#             for allowedRole in allowedRoles:
#                 try:
#                     if allowedRole in request.roles:
#                         print('kk')
#                         checkAuthorization = True
#                         return ViewFuntion(request,*args,**kwargs)
#                 except:
#                     return Response({"message":"bạn không có quyền truy cập"},status=status.HTTP_403_FORBIDDEN)
#             if not checkAuthorization:
#                 return Response({"message":"bạn không có quyền truy cập"},status=status.HTTP_403_FORBIDDEN)
#         return wrap
#     return decorator


def RoleRequest(allowedRoles=None):
    def decorator(ViewFunction):
        def wrapper(request, *args, **kwargs):
            if allowedRoles is None:
                # If no roles are specified, allow access to all users
                return ViewFunction(request, *args, **kwargs)
            else:
                # Check if user's role is in allowedRoles list
                if hasattr(request, 'roles') and set(request.roles).intersection(set(allowedRoles)):
                    # User has an allowed role, allow access to view
                    return ViewFunction(request, *args, **kwargs)
                else:
                    # User does not have an allowed role, deny access and return an error response
                    return Response({"message": "Bạn không có quyền truy cập."}, status=status.HTTP_403_FORBIDDEN)
        return wrapper
    return decorator
