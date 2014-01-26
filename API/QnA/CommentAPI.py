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
            return get_parent_message(request.GET.get("parentId"), request.GET.get("isQuestion"), request.user.organization.organization_id)
        elif order == "id":
            return get_by_id(request.GET.get("messageId"), request.user.organization.organization_id)
        else:
           return Response({"messages": "No correct order type provided.", "identifier": "order"}, 400)

    def get_all(self, organization):
        '''
        Get all comments.
        @params
            organization, Organization: Organization object.

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
        try:
            data = []
            comment_data = Comment.objects.filter(organization=organization)
            for comment in comment_data:
                data.append(comment.serialize())
            return Response({"comments": data}, 200)
        except:
            return Response({"messages": "No comments related to this organization", "identifier": "organization_id"}, 400);

    def get_by_id(self, comment):
        '''
        Get Comment by id.

        @params
            comment, string: Message id of comments to retrieve.
        '''
        return get_message_by_id(Comment, comment)

    def get_related_to_parent(self, parent_id, organization_id, limit=3, order="latest"):
        '''
        Get all comments related to given parentid (questions/answeers messageId).

        @params
            parentid, string: Parent id.
            organization, int: Organization id.
            limit, int: Limits the amount of results returned.
            order, string: Order type.
        @example
            /comments/?parentId=2&organizationId=1&limit=5&order=oldest
        @return
            200: Returned comments related to given parentid.
            204: No comments with given parentid.
            400: Parent id is not int or cannot be converted to int.
        '''
        messages = []
        try:
            data = []
            parent_id = int(parent_id)
            if not isinstance(limit, int) or limit < 0:
                messages.append(compose_message("Limit value is not positive integer.", "limit"))
            if not isinstance(organization_id, id) or organization_id < 0:
                messages.append(compose_message("Organization id is not positive integer.", "organization_id"))
            if parent_id < 0:
                raise ValueError()
            order_by = "pub_date"
            if order == "oldest":
                order_by = "-pub_date"
            comments = Comment.objects.filter(parent_id=parent_id).filter(organization=organization_id).order_by(order_by)[:limit]
            for comment in comments:
                data.append(comment.serialize())
            return Response({"comments": data}, 200)
        except ValueError:
            return Response({"messages": [{"content": "Parent id is not positive integer.", "identifier": "parentId"}]}, 400)
        except:
            return Response({"messages": "No comments exist with given parentid.", "identifier": "parentId"}, 204)

    def get_parent_message(self, parentid, isquestion, organization):
        '''
        Get parent of comment which has messageId equal to parentid.
        isquestion defines whether parent is question or not.

        For more info check get_message_by_id() in view_utils.

        @example
            /comments/?parentId=34&isQuestion=true
        @params
            parentid, string: Parent id for this comment.
            isquestion, string: Boolean value, either "true" or "false".
            organization, int: Organization id.
        @return
            400: If isquestion is none or isquestion is not string.

        '''
        if isquestion is None:
            return Response({"messages": "No value for isQuestion provided.", "identifier": "isQuestion"}, 400)
        if not isinstance(isquestion, basestring):
            return Response({"messages": "Is question is not string.", "identifier": "isQuestion"}, 400)
        if isquestion == "true" or question == "True":
            return get_message_by_id(Question, parentid, organization)
        elif isquestion == "false" or question == "False":
            return get_message_by_id(Answer, parentid, organization)
        else:
            return  Resonse({"messages": "Given value for isquestion is not true or false.", "identifier": "isquestion"}, 400)

