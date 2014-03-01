# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response

from QnA.models import Answer, User, Question
from QnA.serializers import MessageSerializerPOSTAnswer


class AnswerAPI(APIView):

    def post(self, request, rid):
        '''
        @example
            {
                "content": "Example answer modified",
            }
        '''
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
            return Response("Answer succesfully created.", 201)
        else:
            return Response(serializer.errors, 400)

        raise exc.ParseError("Answer could not be created.")
