# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions as exc

from QnA.models import User, Tag, Keyword
from QnA.serializers import CourseSerializerPOST, CourseSerializerGET
from QnA.exceptions import NotFound
from QnA.view_utils import order_messages, get_message_by_id, post_abstract_message


class CourseAPI(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        '''
        This method saves new question into database
        @params (this means body parameters, not autoinserted by django or other methods)
            title, string: title of the Question
            content, string: content text of the Question
            messageId, positive integer: message id of the Question. For client: set this only if you are updating old message. save() method
            will give new messageId for new messages!
        @example:
            {
                "name": string,
                "code": string,
                "categories": [
                    {"title"},
                    {}
                ]
            }
        @perm
            member: any member can post an question
        '''


        serializer = CourseSerializerPOST(data=request.DATA, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            print serializer.object
            get_serializer = CourseSerializerGET(serializer.object)
            print "DATA:", get_serializer.data
            return Response(get_serializer.data, 201)
        else:
            return Response(serializer.errors, 400)

        raise exc.ParseError("Question could not be created.")