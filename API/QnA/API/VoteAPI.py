# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from QnA.models import Vote
from QnA.serializers import VoteSerializerPOST
from QnA.utils import compose_message, create_message


class VoteAPI(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        '''
        This method saves a vote for a question or answer matching the given message_id
        @params
            direction, integer: vote value, can be either 1 or -1
            messageId, positive integer: message id of the target
        @example:
            {
                "direction": 1,
                "message_id": 3
            }
        @perm
            member: any member can vote
        @return
            201: Created, the vote was succesfully created
            400: Bad request, parameters were missing or wrong type
                list of appropriate error messages
                example: {"messages":[{"content": "An example error message.", "identifier": "example"}]}
            401: Unauthorized, the user has to be logged in to perform this action
                list of appropriate error messages
                example: {"messages":[{"content": "An example error message.", "identifier": "example"}]}
        '''

        data = {
            "user": request.user.pk,
            "message_id": request.DATA.get("message_id", None),
            "direction": request.DATA.get("direction", None)
        }

        # check for existing vote
        tryvote = Vote.objects.filter(
            message_id=request.DATA.get("message_id"),
            user=request.user)
        if tryvote:
            # vote exists with same direction
            if tryvote[0].direction == request.DATA.get("direction"):
                return Response(compose_message("Vote exists already"), 403)
            # vote needs to be updated
            else:
                serializer = VoteSerializerPOST(tryvote[0], data=data)
        else:
            serializer = VoteSerializerPOST(data=data)

        # validate and save
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
        else:
            return Response(serializer.errors, 400)
