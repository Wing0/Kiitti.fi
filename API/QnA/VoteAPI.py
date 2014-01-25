from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import *
import json

class VoteAPI(APIView):

    def get(self, request):
        data = []
        votedata = Vote.objects.all()
        for vote in votedata:
            data.append(vote.serialize())
        return Response({"votes": data}, 200)

    def post(self, request):
        data = json.loads(request.body)
        vote = Vote()
        if 'rate' in data:
            vote.rate = data["rate"]
        else:
            rate = 0
        if 'userId' in data:
            vote.user_id = data["userId"]
        else:
            return Response({"messages": {
                "type": "alert",
                "content": "User id has to be a positive integer",
                "identifier": "user_id"}}, 200)
        if 'messageId' in data:
            vote.message_id = data["messageId"]
        else:
            return Response({"messages": {
                "type": "alert",
                "content": "Message id has to be a positive integer",
                "identifier": "message_id"}}, 200)
        vote.save()
        return Response(200)
