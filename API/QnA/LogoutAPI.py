from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from QnA.utils import *
import json

from view_utils import *

class LogoutAPI(APIView):

    #logout
    def post(self, request):
        try:
            logout(request)
            return Response({}, 200)
        except:
            return Response(create_message("Logout failed."), 500)

    def get(self, request):
        logout(request)
        return Response({}, 200)
