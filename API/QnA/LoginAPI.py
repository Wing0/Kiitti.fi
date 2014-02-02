from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from QnA.utils import *
import json

class LoginAPI(APIView):

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        '''
        Log the user in using an username and password

        @return:
            200: Logging in was successful or user was already logged in
                list of appropriate error messages if already logged in
                @example:
                    {
                        "messages":[{"content":"An example error message.","identifier":"example"}]
                    }

            403: User does not have permission to log in (banned)
                list of appropriate error messages
                example:{
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }

            404: User was not found
                list of appropriate error messages
                example:{
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }

            400: Invalid request, parameters were missing or wrong type
                list of appropriate error messages
                example:{
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }

        '''
        if request.user.is_authenticated():
            return Response({"messages":[{"content":"User was already logged in.","identifier":""}]},200)

        data = json.loads(request.body)
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
        return Response({"messages":[{"content":"Username and/or password was missing.","identifier":""}]}, 400)


    # GetCsrfToken
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        '''
        Check if user is logged in or not

        @return:
            200: Request was successful, user is logged in
                return user object serlialization
                @example:
                    {
                        "user":{
                                  "username":"test",
                                  "password":"test",
                                  "organizationId":1,
                                  "email":"test@test.test",
                                  "firstName":"test",
                                  "lastName":"test"
                                }
                    }

            401: Unauthorized, the user has to be logged in to perform this action
                list of appropriate error messages
                example:{
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }

        '''
        if request.user.is_authenticated():
            return Response({"user":request.user.serialize()},200)
        else:
            return Response(create_message("User is not logged in."), 401)

