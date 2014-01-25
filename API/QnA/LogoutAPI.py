from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.views import APIView
import json

class LogoutAPI(APIView):

    #logout
    def post(self, request):
        logout(request)
        return Response({}, 200)
