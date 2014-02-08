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
        @params
            isQuestion: If true comment is question comment.
            parentId: Message id of parent message.
            content: Content of this comment.
        @example
            NOTE: Provide messageId only if you liked to update new version.
            {
                "isQuestion": "false",
                "content": "I am important comment!11!!1",
                "messageId": 2,
                "parentId": 1
            }
        @perm
            No idea... Currently no perms.
        @return
            201: If sent data is valid and new Comment was created successfully. No messages returned.
            400: If sent data is not valid.
            401: If user is not logged in.
        '''
        if not request.user.is_authenticated():
            return Response(create_message("You must log in to post comments."), 401)
        data = json.loads(request.body)
        messages = []
        abs_data = post_abstract_message(Comment(), data)
        parent_id = data["parentId"]
        if parent_id is None:
            raise Exception()
        try:
            parent_id = int(parent_id)
        except Exception:
            messages.append(compose_message("Parent id must be positive integer.", "parentId"))
        question = data["isQuestion"]
        if question == "True" or question == "true":
            question = True
        elif question == "False" or question == "false":
            question = False
        else:
            messages.append(compose_message("Is question must be boolean.", "isQuestion"))
        if len(messages) == 0:
            abs_data.is_question_comment = question
            abs_data.organization = request.user.organization
            abs_data.user = request.user
            abs_data.parent_id = parent_id
            msg = abs_data.validate()
            if len(msg) == 0:
                abs_data.save()
                return Response(create_message("New comment was created successfully."), 201)
            else:
                return Response({"messages": msg}, 400)
        return Response({"messages": messages}, 400)

    def get(self, request):
        '''
        Get comments.

        Comments can be searched by message_id or by its parents message_id.
        Get parameter called 'order' defines how comments are searched.
        Allowed order parameters are: order=id, order=parent or no order type (None).
        If order=id is given you must also provide parameter messageId (ex. messageId=3).
        If order=parent is given you must provide parameter parentId (ex. parentId=3)

        @params
            isQuestion: Determines whether comment belongs to question.
            parentId: Id of parent message.
            messageId: Id of comment to get.
            limit: Maximum amount of comments to return.
            order:
                parent: Use for testing
                id: Get comment with messageId
            sort:
                latest: Newest comments are first.
                oldest: Oldest comments are first.

        @example
        /comments?order=parent&isQuestion=false&parentId=2&sort=latest&limit=5

        ^^Returns 5 newest comments which have Answer with message_id=2 as a parent.

        @returns
            200: If content was found.
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

            400: If order has invalid value.
            401: If user is not logged in.
            403: If user has no permission to perfrom asked action.
            404: If comments was not found with given id.
        '''
        order = request.GET.get("order")
        if not request.user.is_authenticated():
            return Response(create_message("You must be logged in to request comments."), 401)
        if order is None:
            return self.get_all(request.user.organization.organization_id)
        elif order == "parent":
            parent = string_to_int(request.GET.get("parentId"))
            is_question = string_to_boolean(request.GET.get("isQuestion"))
            sort = string_to_int(request.GET.get("sort"))
            limit = string_to_int(request.GET.get("limit"))
            if limit is None:
                limit = 3
            if sort is None:
                sort = "latest"
            return self.get_by_parent(parent, is_question, request.user.organization.organization_id, limit, sort)
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

    def get_by_id(self, comment, organization):
        '''
        Get Comment by id.

        For more info check get_message_by_id() in view_utils.

        @params
            comment, string: Message id of comments to retrieve.
        '''
        return get_message_by_id(Comment, comment, organization)


    def get_by_parent(self, parent_id, is_question, organization_id, limit=3, order="latest"):
        '''
        Get all comments related to given parentid (question/answer messageId).

        @params
            parent_id, int: Parent id.
            is_question, bool: If true parent message is question.
            organization, int: Organization id.
            limit, int: Limits the amount of results returned.
            order, string: Order type.
        @example
            /comments/?parentId=2&organizationId=1&limit=5&order=oldest
        @return
            200: Returned comments related to given parentid.
            400: Bad request. Returned error messages.
            403: If user has no permission.
            404: If content was not found.
        '''
        messages = []
        if not isinstance(parent_id, int) or parent_id < 0:
            messages.append(compose_message("Parent id must be positive integer.", "parent_id"))
        if not isinstance(limit, int) or limit < 0:
            messages.append(compose_message("Limit value is not positive integer.", "limit"))
        if not isinstance(organization_id, int) or organization_id < 0:
            messages.append(compose_message("Organization id is not positive integer.", "organization_id"))
        if not isinstance(order, basestring):
            messages.append(compose_message("Order is not string", "order"))
        if not isinstance(is_question, bool):
            messages.append(compose_message("Is question value is not boolean.", "is_question"))
        if len(messages) == 0:
            order_by = "-created"
            if order == "oldest":
                order_by = "created"
            try:
                try:
                    message = None
                    if is_question:
                        message = Question.objects.get(message_id=parent_id)
                    else:
                        message = Answer.objects.get(message_id=parent_id)
                    if organization_id != message.organization.organization_id:
                        return Response(create_message("You are not allowed to perform this action."), 403)
                except Exception:
                    return Response(create_message("No messages found with given parent id.", "parent_id"), 404)
                data = []
                comments = Comment.objects.filter(parent_id=parent_id).order_by(order_by)[:limit]
                for comment in comments:
                    data.append(comment.serialize())
                return Response({"comments": data}, 200)
            except Exception, e:
                return Response({"comments": e.message}, 200)
        return Response({"messages": messages}, 400)
