# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions as exc

from QnA.models import Vote
from QnA.serializers import VoteSerializerPOST
from QnA.utils import compose_message, create_message


class VoteAPI(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, message_type):
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
        '''

        if not message_type.lower() in ["question", "answer", "comment"]:
            raise exc.ParseError("Must have type question/answer/comment in URL.")
        if not request.DATA.get('message_id', None):
            raise exc.ParseError("Must have message_id.")

        try:
            content_type = ContentType.objects.get(name=message_type)
            voteobject = content_type.get_object_for_this_type(rid=request.DATA['message_id'])
        except:
            raise exc.ParseError("Cannot find message to vote.")

        request.DATA['user'] = request.user.pk # important

        # check for existing vote
        tryvote = Vote.objects.filter(
            head_type__model=message_type,
            head_id=voteobject.pk,
            user=request.user)

        # update old
        if tryvote:
            tryvote[0].direction = request.DATA['direction']
            tryvote.save()
            return Response("Vote updated.", 200)

        # create new
        vote = Vote(direction=request.DATA['direction'],
                    user=request.user,
                    head_type=content_type,
                    head_id=voteobject.pk)
        vote.save()

        return Response("vote created", 201)

        # Better saving method in development:

        # if tryvote:
        #     # vote exists with same direction
        #     if tryvote[0].direction == request.DATA.get("direction"):
        #         raise exc.ParseError("Vote exists already.")
        #     # vote needs to be updated
        #     else:
        #         serializer = VoteSerializerPOST(tryvote[0], data=request.DATA)
        # else:
        #     serializer = VoteSerializerPOST(data=request.DATA)

        # # validate and save
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, 201)
        # else:
        #     return Response(serializer.errors, 400)
