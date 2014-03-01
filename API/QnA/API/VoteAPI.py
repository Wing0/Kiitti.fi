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

    def post(self, request, content_type=None, rid=None):
        """
        @example:
            {
                "direction": 1
            }
        """

        try:
            content_type = ContentType.objects.get(name=content_type)
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
            # update old
            tryvote = Vote.objects.get(head_type=content_type.pk,
                                       head_id=vote_target_object.pk,
                                       user=request.user)
            serializer = VoteSerializerPOST(tryvote, data=data_to_serialize)
            if serializer.is_valid():
                serializer.save()
                return Response("Vote updated.", 200)
        except Vote.DoesNotExist:
            # create new
            serializer = VoteSerializerPOST(data=data_to_serialize)
            if serializer.is_valid():
                serializer.save()
                return Response("Vote created.", 201)

        raise exc.ParseError("Vote could not be created.")
