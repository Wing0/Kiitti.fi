# -*- coding: utf-8 -*-

from django.contrib.auth import logout

from rest_framework.views import APIView
from rest_framework.response import Response


class LogoutAPI(APIView):

    def post(self, request):
        try:
            logout(request)
            return Response({}, 200)
        except:
            return Response(create_message("Logout failed."), 500)

    def get(self, request):
        logout(request)
        return Response({}, 200)
