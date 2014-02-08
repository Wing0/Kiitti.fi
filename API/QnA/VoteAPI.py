from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import *
from QnA.utils import *
import json

class VoteAPI(APIView):

    def get(self, request):
        data = []
        votedata = Vote.objects.all()
        for vote in votedata:
            data.append(vote.serialize())
        return Response({"votes": data}, 200)

    def post(self, request):
        '''
        This method saves a vote for a question or answer matching the given message_id
        @params
            direction, integer: vote value, can be either 1 or -1
            messageId, positive integer: message id of the target
        @example:
            {
                "direction": 1,
                "messageId":3
            }
        @perm
            member: any member can vote
        @return
            201: Created, the vote was succesfully created
            400: Bad request, parameters were missing or wrong type
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }
            401: Unauthorized, the user has to be logged in to perform this action
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
        '''
        messgaes = []
        if not request.user.is_authenticated():
            return Response({"messages":create_message("User must be logged in.")}, 401)
        else:
            data = json.loads(request.body)
            vote = Vote()

            vote.direction = data.get("direction")
            if not vote.direction in [1,-1]:
                messages.append(compose_message("Vote direction must be either 1 or -1.","direction"))

            vote.message_id = data.get("messageId")
            if not isinstance(vote.message_id, int) or vote.message_id < 0:
                messages.append(compose_message("Message id must be a positive integer.","direction"))
            else:
                message =
                return Response({"messages": {
                    "type": "alert",
                    "content": "Message id has to be a positive integer",
                    "identifier": "message_id"}}, 200)
            vote.save()
            return Response(200)
