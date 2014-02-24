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
        parent_id = string_to_int(data.get("parentId"))
        if parent_id is None:
            messages.append(compose_message("Parent id must be positive integer.", "parentId"))
        question = string_to_boolean(data.get("isQuestion"))
        if question is None:
            messages.append(compose_message("IsQuestion must be boolean.", "isQuestion"))
        if len(messages) == 0:
            abs_data.is_question_comment = question
            abs_data.organization = request.user.organization
            abs_data.user = request.user
            abs_data.parent_id = parent_id
            msg = abs_data.validate()
            if len(msg) == 0:
                if abs_data.message_id is None:
                    abs_data.save()
                    return Response(abs_data.serialize(), 201)
                else:
                    abs_data.save_changes()
                    return Response(abs_data.serialize(), 201)
            else:
                return Response({"messages": msg}, 400)
        return Response({"messages": messages}, 400)

    def get(self, request):
        '''
        Get comments.

        Comments can be searched by message_id or by its parents message_id.
        If searched by message_id, allowed parameters are:
            - messageId
            - (Additional) history
        If searched by parent_id, allowed parameters are:
            - parentId, isQuestion
            - (Additional) limit, sort

        @params
            messageId: Id of comment to get.
            history: If true version history is included

            isQuestion: Determines whether comment belongs to question.
            parentId: Id of parent message.
            limit: Maximum amount of comments to return.
            sort:
                latest: Newest comments are first.
                oldest: Oldest comments are first.

        @examples
        /comments?isQuestion=false&parentId=2&sort=latest&limit=5
        ^^Returns 5 newest comments which have Answer with message_id=2 as a parent.

        /comments?messageId=1&history=true
        ^^Returns comment with message_id=1 with all versions.

        @returns
            200: If content was found.
            example:
                {
                    "comments":[
                        {
                            "created": "2014-02-08T15:11:59",
                            "organizationId": 0,
                            "parentId": 5,
                            "content": "dasfasdasfasdasdasfasfasdas",
                            "version": 1,
                            "messageId": 0
                            "user": {
                                "username": "test",
                                "reputation": 0,
                                "lastLogin": "2014-02-02T19:00:31.568Z",
                                "firstName": "test",
                                "created": "2014-01-25T18:34:35Z",
                                "lastName": "test",
                                "userId": 2,
                                "email": "test@test.test"
                            },
                        }
                    ]
                }

            400: If parameters are invalid.
            401: If user is not logged in.
            403: If user has no permission to perfrom asked action.
            404: If comments were not found.
        '''
        if not request.user.is_authenticated():
            return Response(create_message("You must be logged in to request comments."), 401)
        if request.GET.get("parentId"):
            parent = string_to_int(request.GET.get("parentId"))
            is_question = string_to_boolean(request.GET.get("isQuestion"))
            sort = string_to_int(request.GET.get("sort"))
            limit = string_to_int(request.GET.get("limit"))
            if limit is None:
                limit = 3
            if sort is None:
                sort = "latest"
            return self.get_by_parent(parent, is_question, request.user.organization.organization_id, limit, sort)
        elif request.GET.get("messageId"):
            history = string_to_boolean(request.GET.get("history"))
            if history is None:
                history = False
            return self.get_by_id(request.GET.get("messageId"), request.user.organization.organization_id, history)
        else:
           return self.get_all(request.user.organization.organization_id)

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
                        "created": "2014-02-08T15:11:59",
                        "organizationId": 0,
                        "parentId": 5,
                        "content": "dasfasdasfasdasdasfasfasdas",
                        "version": 1,
                        "messageId": 0
                        "user": {
                            "username": "test",
                            "reputation": 0,
                            "lastLogin": "2014-02-02T19:00:31.568Z",
                            "firstName": "test",
                            "created": "2014-01-25T18:34:35Z",
                            "lastName": "test",
                            "userId": 2,
                            "email": "test@test.test"
                        },
                    }
                ]
            }
            404: If no comments exist.
        '''
        try:
            data = []
            comment_data = Comment.objects.filter(organization=organization)
            for comment in comment_data:
                data.append(comment.serialize())
            return Response({"comments": data}, 200)
        except:
            return Response(create_message("No comments related to this organization", "organization_id"), 404);

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
                return Response({"messages": e.message}, 400)
        return Response({"messages": messages}, 400)
