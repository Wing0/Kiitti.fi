# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions as exc

from QnA.models import Answer, User, Question
from QnA.serializers import MessageSerializerPOSTAnswer, AnswerSerializerGET


class AnswerAPI(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, rid):
        '''
        @example
            {
                "content": "Example answer modified",
            }
        '''
        # find question first
        try:
            question = Question.objects.get(rid=rid)
        except:
            raise exc.ParseError("Cannot find question to answer.")

        data_to_serialize = {
            "user": request.user.pk,
            "content": request.DATA.get('content', None),
            "head": {
                "question": question.pk,
                "user": request.user.pk
            }
        }

        serializer = MessageSerializerPOSTAnswer(data=data_to_serialize)

        if serializer.is_valid():
            serializer.save()
            answer = serializer.object.head
            get_serializer = AnswerSerializerGET(answer)
            return Response(get_serializer.data, 201)
        else:
            return Response(serializer.errors, 400)

        raise exc.ParseError("Answer could not be created.")
