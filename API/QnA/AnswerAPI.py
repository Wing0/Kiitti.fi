from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import *
from QnA.view_utils import *
import json

class AnswerAPI(APIView):

    def get(self, request):
        data = []
        answer_data = Answer.objects.all()
        for answer in answer_data:
            data.append(answer.serialize())
        return Response({"answers": data}, 200)

    def post(self, request):
        data = json.loads(request.body)
        messages = {}
        try:
            abs_data = post_abstract_message(Answer(), data)
        except Exception, e:
            return Response({"messages": {"type": "alert", "content": str(e), "identifier": ""}}, 200)

        if 'accepted' in data:
            abs_data.accepted = data["accepted"]
        else:
            abs_data.accepted = False
        if 'questionId' in data:
            abs_data.question_id = data["questionId"]
        else:
            abs_data.question_id = None
        valid, messages = abs_data.validate()
        if valid:
            abs_data.save()
        return Response({"messages": messages}, 200)
