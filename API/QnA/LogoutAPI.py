from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from QnA.utils import *
import json

class LogoutAPI(APIView):

    def post(self, request):
        logout(request)
        return Response({}, 200)

    def get(self, request):
        logout(request)
        return Response({}, 200)
