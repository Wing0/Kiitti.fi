from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.views import APIView
import json

class LoginAPI(APIView):

    #login
    def post(self, request):
        data = json.loads(request.body)
        if data.get("username") and data.get("password"):
            username = data.get('username')
            password = data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    Response({},200)
                else:
                    Response({"messages":[{"content":"User is banned.","identifier":""}]},401)
            else:
                Response({"messages":[{"content":"Username and/or password was incorrect.","identifier":""}]},404)
        return Response({"messages":[{"content":"Username and/or password was missing.","identifier":""}]}, 404)
