# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions as exc

from QnA.utils import create_message
from QnA.serializers import UserSerializerGET


class LoginAPI(APIView):

    def get(self, request):
        '''
        Check if user is logged in or not

        @return:
            200: Request was successful, user is logged in
                return user object serlialization
                @example:
                    {
                        "user": {
                          "username": "test",
                          "organizationId": 1,
                          "email": "test@test.test",
                          "firstName": "test",
                          "lastName": "test"
                        }
                    }

            401: Unauthorized, the user has to be logged in to perform this action
                list of appropriate error messages
                example:{
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }

        '''
        if request.user.is_authenticated():
            serializer = UserSerializerGET(request.user)
            return Response(serializer.data, 200)
        else:
            return Response(create_message("User is not logged in."), 401)
