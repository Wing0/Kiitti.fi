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
        '''
        Get comments.
        '''
        order = request.GET.get("order")
        if order is None:
            return Response({"messages": "No order type provided.", "identifier": "order"}, 400)
        elif order == "parent":
            return get_parent_message(request.GET.get("parentId"), request.GET.get("isQuestion"))
        elif order == "id":
            return get_by_id(request.GET.get("messageId"))
        else:
           return Response({"messages": "No correct order type provided.", "identifier": "order"}, 400)

    def get_all(self):
        '''
        Get all comments.
        @return
            200: All Comments ever created.
            example:
            {
                "comments":[
                    {
                        "messageId": 3,
                        "content": "I am very important content of random comment.",
                        "parentId": 1,
                        "isQuestion": "true",
                        "version": 0,'
                        "user":{
                            "username": "admin",
                            "firstname": "Admin",
                            "lastname": "Adminen",
                            "email": "admin@admin.org",
                            "reputation": 0,
                            "userId": 1,
                            "created": "2014-01-25T18:28:28.520Z"
                        }
                    }
                ]
            }
        '''
        data = []
        comment_data = Comment.objects.all()
        for comment in comment_data:
            data.append(comment.serialize())
        return Response({"comments": data}, 200)

    def get_by_id(self, comment):
        '''
        Get Comment by id.

        @params
            comment, string: Message id of comments to retrieve.
        '''
        return get_message_by_id(Comment, comment)

    def get_related_to_parent(self, parentid):
        '''
        Get all comments related to given parentid (questions/answeers messageId).

        @params
            parentid, string: Parent id.
        @example
            /comments/?parentId=2
        @return
            200: Returned comments related to given parentid.
            204: No comments with given parentid.
            400: Parent id is not int or cannot be converted to int.
        '''
        try:
            data = []
            parentid = int(parentid)
            if parentid < 0:
                raise ValueError()
            comments = Comment.objects.filter(parent_id=parentid)
            for comment in comments:
                data.append(comment.serialize())
            return Response({"comments": data}, 200)
        except ValueError:
            return Response({"messages": "Parent id is not positive integer.", "identifier": "parentId"}, 400)
        except:
            return Response({"messages": "No comments exist with given parentid.", "identifier": "parentId"}, 204)

    def get_parent_message(self, parentid, isquestion):
        '''
        Get parent of comment which has messageId equal to parentid.
        isquestion defines whether parent is question or not.

        For more info check get_message_by_id() in view_utils.

        @example
            /comments/?parentId=34&isQuestion=true
        @params
            parentid, string: Parent id for this comment.
            isquestion, string: Boolean value, either "true" or "false".
        @return
            400: If isquestion is none or isquestion is not string.

        '''
        if isquestion is None:
            return Response({"messages": "No value for isQuestion provided.", "identifier": "isQuestion"}, 400)
        if not isinstance(isquestion, basestring):
            return Response({"messages": "Is question is not string.", "identifier": "isQuestion"}, 400)
        if isquestion == "true" or question == "True":
            return get_message_by_id(Question, parentid)
        else if isquestion == "false" or question == "False":
            return get_message_by_id(Answer, parentid)
        else

