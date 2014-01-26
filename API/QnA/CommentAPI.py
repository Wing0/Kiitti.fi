from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import *
from QnA.view_utils import *
import json

class CommentAPI(APIView):

    def post(self, request):
        data = json.loads(request.body)
        messages = {}
        try:
            abs_data = post_abstract_message(Comment(), data)
        except Exception, e:
            return Response({"messages": {"type": "alert", "content": str(e), "identifier": ""}}, 200)

        parent_id = data["parentId"]
        abs_data.parent_id = parent_id
        abs_data.save()
        return Response(200)

    def get(self, request):
        data = []
        comment_data = Comment.objects.all()
        for comment in comment_data:
            data.append(comment.serialize())
        return Response({"comments": data}, 200)
