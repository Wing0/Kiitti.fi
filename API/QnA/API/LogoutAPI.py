from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.views import APIView


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
