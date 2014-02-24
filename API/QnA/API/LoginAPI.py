# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response

from QnA.utils import create_message


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
            return Response(request.user.serialize(), 200)
        else:
            return Response(create_message("User is not logged in."), 401)
