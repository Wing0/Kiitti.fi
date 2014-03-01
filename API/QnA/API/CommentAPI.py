# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions as exc

from QnA.models import Comment
from QnA.serializers import MessageSerializerPOSTComment


class CommentAPI(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, content_type=None, rid=None):
        """
        @example
            {
                "content": "I am important comment!11!!1"
            }
        """

        try:
            content_type = ContentType.objects.get(name__iexact=content_type)
            comment_target_object = content_type.get_object_for_this_type(rid=rid)
        except:
            raise exc.ParseError("Cannot find message to comment.")

        data_to_serialize = {
            "user": request.user.pk,
            "content": request.DATA.get('content', None),
            "head": {
                "head_id": comment_target_object.pk,
                "head_type": content_type.pk,
                "user": request.user.pk
            }
        }

        serializer = MessageSerializerPOSTComment(data=data_to_serialize)

        if serializer.is_valid():
            serializer.save()
            return Response("Comment succesfully created.", 201)
        else:
            return Response(serializer.errors, 400)

        raise exc.ParseError("Comment could not be created.")
