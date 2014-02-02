from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import *
from QnA.view_utils import *
from QnA.utils import *
import json

class CommentAPI(APIView):

    def post(self, request):
        '''
        Example in get_all()-method.
        '''
        data = json.loads(request.body)
        messages = {}
        abs_data = post_abstract_message(Comment(), data)
        parent_id = data["parentId"]
        abs_data.organization = request.user.organization
        abs_data.user = request.user
        abs_data.parent_id = parent_id
        abs_data.save()
        return Response(200)

    def get(self, request):
        '''
        Get comments.
        @returns
            403: If user is not logged in.
            400: If order has invalid value.
        '''
        order = request.GET.get("order")
        if not request.user.is_authenticated():
            return Response(create_message("You must be logged in to request comments."), 403)
        if order is None:
            return self.get_all(request.user.organization.organization_id)
        if order == "parent":
            return self.get_parent_message(request.GET.get("parentId"),
                request.GET.get("isQuestion"), request.user.organization.organization_id)
        elif order == "id":
            return self.get_by_id(request.GET.get("messageId"), request.user.organization.organization_id)
        else:
           return Response(create_message("No order type provided.", "order"), 400)

    def get_all(self, organization):
        '''
        Get all comments.
        @params
            organization, int: Organization id.

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
                        "version": 0,
                        "userId": 2
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
            return Response(create_message("No comments related to this organization", "organization_id"), 400);

    def get_by_id(self, comment):
        '''
        Get Comment by id.

        For more info check get_message_by_id() in view_utils.

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
            400: Bad request. Returned error messages.
        '''
        messages = []
        if not isinstance(parent_id, int) or parent_id < 0:
            messages.append(compose_message("Parent id must be positive integer.", "parent_id"))
        if not isinstance(limit, int) or limit < 0:
            messages.append(compose_message("Limit value is not positive integer.", "limit"))
        if not isinstance(organization_id, id) or organization_id < 0:
            messages.append(compose_message("Organization id is not positive integer.", "organization_id"))
        if not isinstance(order, basestring):
            messages.append(compose_message("Order is not string", "order"))
        if len(messages) == 0:
            order_by = "pub_date"
            if order == "oldest":
                order_by = "-pub_date"
            data = []
            comments = Comment.objects.filter(parent_id=parent_id).filter(organization=organization_id).order_by(order_by)[:limit]
            for comment in comments:
                data.append(comment.serialize())
            return Response({"comments": data}, 200)
        return Response({"messages": messages}, 400)

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
            400: Bad request. Returned error messages.

        '''
        messages = []
        temp = False
        if isquestion == "true" or question == "True":
            temp = True
        if not isinstance(history, bool):
            messages.append(compose_message("History must be boolean value.", "history"))
        if len(messages) == 0:
            if temp:
                return get_message_by_id(Question, parentid, organization)
            else:
                return get_message_by_id(Answer, parentid, organization)
        return Response({"messages": messages}, 400)

