from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
import json

class LoginAPI(APIView):

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        if request.user.is_authenticated():
            return Response({"messages":[{"content":"User was already logged in.","identifier":""}]},200)

        data = json.loads(request.body)
        print data
        if data.get("username") and data.get("password"):
            username = data.get('username')
            password = data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return Response({},200)
                else:
                    return Response({"messages":[{"content":"User is banned.","identifier":""}]},403)
            else:
                return Response({"messages":[{"content":"Username and/or password was incorrect.","identifier":""}]},404)
        return Response({"messages":[{"content":"Username and/or password was missing.","identifier":""}]}, 404)


    # GetCsrfToken
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        if user.is_authenticated()
            return Response({"user":request.user.serialize()},200)
        else:
            return Response(create_message("User is not logged in.")}, 401)

