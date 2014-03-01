# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions as exc

from QnA.models import Vote
from QnA.serializers import VoteSerializerPOST


class VoteAPI(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, content_type=None, rid=None):
        """
        @example:
            {
                "direction": 1
            }
        """

        try:
            content_type = ContentType.objects.get(name__iexact=content_type)
            vote_target_object = content_type.get_object_for_this_type(rid=rid)
        except:
            raise exc.ParseError("Cannot find message to vote.")

        data_to_serialize = {
            "user": request.user.pk,
            "direction": request.DATA.get('direction', None),
            "head_id": vote_target_object.pk,
            "head_type": content_type.pk,
        }

        try:
            # TODO: move to PUT-method
            # update old
            tryvote = Vote.objects.get(head_type=content_type.pk,
                                       head_id=vote_target_object.pk,
                                       user=request.user)
            serializer = VoteSerializerPOST(tryvote, data=data_to_serialize)
            status = 200
        except Vote.DoesNotExist:
            # create new
            serializer = VoteSerializerPOST(data=data_to_serialize)
            status = 201

        if serializer.is_valid():
            serializer.save()
            response = {
                "votes_up": Vote.objects.filter(head_id=vote_target_object.pk,
                                                head_type=content_type.pk,
                                                direction=1).count(),
                "votes_down": Vote.objects.filter(head_id=vote_target_object.pk,
                                                head_type=content_type.pk,
                                                direction=-1).count(),
                "user_vote": data_to_serialize['direction']
            }
            return Response(response, status)

        raise exc.ParseError("Vote could not be created.")
