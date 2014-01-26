from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import *
from QnA.view_utils import *
import json

from view_utils import post_abstract_message, exclude_old_versions

class AnswerAPI(APIView):

    def get(self, request):
        '''
        This method mediates the task to correct function.
        Further information in helper method docstring
        '''
        if request.GET.get("questionId") != None:
            return self.by_question_id(request, request.GET.get("questionId"), request.GET.get("limit"), request.GET.get("order"))
        elif request.GET.get("authorId") != None:
            return self.by_author_id(request, request.GET.get("authorId"), request.GET.get("limit"), request.GET.get("order"))
        # ToDo: get all latest/best answers?
        else:
            return Response({"user":request.user.serialize(), "questionId":request.GET.get("questionId")},404)


    # ToDo: accept an answer -method
    @csrf_exempt
    def post(self, request):
        '''
        This method takes answer information and produces an answer object accordingly.
        @params
            questionId, integer: The id of the question which the answer relates to
            content, string:
            messageId, integer (optional): In case the message is modified, provide the initial messageId
        @example
            {
                "questionId":1,
                "content":"Example answer modified",
                "messageId":3
            }
        @perm
            member: any member can post an answer
        @return
            201: Created, the answer was succesfully created
            400: Bad request, parameters were missing or wrong type
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }
            401: Unauthorized, the user has to be loggend in to perform this action
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
            403: Forbidden, the user does not have permission for the action
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]

        '''
        data = json.loads(request.body)
        messages = []

        ans = post_abstract_message(Answer(), data)
        if request.user.is_authenticated():
            ans.user = request.user
        else:
            messages.append({"content":"User must be logged in.", "identifier":"user"})
            return Response({"messages":messages}, 401)

        ans.accepted = data.get("accepted")
        if ans.accepted == None:
            ans.accepted = False
        if data.get("questionId") != None:
            try:
                q_id = int(data.get("questionId"))
                ans.question_id = q_id
                q = Question.objects.get(message_id=q_id)
                if not q.organization == request.user.organization:
                    messages.append(compose_message("You are not allowed to perform this action."))
                    return Response({"messages":messages}, 403)
            except ValueError:
                messages.append(compose_message("Question id must be positive integer","questionId"))
            except Exception, e:
                messages.append(compose_message("Question was not found.","questionId"))
                return Response({"messages":messages}, 404)

        else:
            messages.append(compose_message("Please provide question id.", "questionId"))
        messages = ans.validate()
        if len(messages) == 0:
            ans.save()
            return Response({"messages": messages}, 201)
        return Response({"messages":messages}, 400)

    def by_question_id(self, request, question_id, limit=10, order="latest"):
        '''
        by_question_id:
        Retrieves all answers related to given question. The order and limit of answers can be chosen.

        @params
            question_id: The id of the question in which the answers are related to
            limit, integer (optional): The maximum number of answers retriveved. Default = 10
            order, string (optional): The method for ordering the retrieved answers. "votes" or "latest". Default="latest".
        @example
            /answers/?questionId=123&limit=4&order="votes"
        @perm
            member: All answer information can be given only for members of the organization
        @return
            200:
                list of retrieved answers
                example: {
                            "answers":[{
                                        "content":"An example answer",
                                        "version":1,
                                        "userId":123,
                                        "created": "2014-01-08T11:05:16",
                                        "modified": "2014-01-08T11:05:16",
                                        "messageId": 4,
                                        "questionId":1,
                                        "accepted":false
                                        }]
                        }
            404: No content found
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }
            400: Bad request, parameters were missing or wrong type
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }
            401: Unauthorized, the user has to be logged in to perform this action
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
            403: Forbidden, the user does not have permission for the action
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
        '''
        messages = []
        if question_id == None:
            messages.append({"content":"A question id has to be provided.","identifier":"questionId"})
        else:
            if not request.user.is_authenticated():
                messages.append({"content":"User must be logged in.", "identifier":"user"})
                return Response({"messages":messages}, 401)
            try:
                # Parameter check and default values
                question_id = int(question_id)
                if question_id < 0:
                    raise ValueError("Value is not positive integer")

                if limit == None:
                    limit = 10
                try:
                    limit = int(limit)
                    if limit < 0:
                        raise ValueError("Value is not positive integer")
                except ValueError:
                    messages.append({"content":"The limit has to be a positive integer.","identifier":"limit"})

                try:
                    q = Question.objects.get(message_id=question_id)
                    if not q.organization == request.user.organization:
                        messages.append(compose_message("You are not allowed to perform this action."))
                        return Response({"messages":messages}, 403)
                except Exception, e:
                    messages.append({"content":"The question was not found. %s" %e,"identifier":"questionId"})
                    return Response({"messages":messages}, 404)
                if order == None:
                    order = "latest"
                if not order in ["latest","votes"]:
                    messages.append({"content":"The order parameter can be only 'latest' or 'votes'","identifier":"order"})

                if len(messages) == 0:
                    answers = list(Answer.objects.filter(question_id=question_id))
                    if len(answers) == 0:
                        messages.append({"content":"The question does not have answers.","identifier":""})
                        return Response({"messages":messages}, 404)

                    answers = exclude_old_versions(answers)
                    if order == "latest":
                        answers.sort(key=lambda x: x.created)

                    return Response({"answers":[ans.serialize() for ans in answers[:limit]], "messages":messages}, 200)

            except ValueError:
                messages.append({"content":"The question id has to be a positive integer.","identifier":"questionId"})
        return Response({"messages":messages}, 400)

    def by_author(self, request, authorId, limit=10, order="latest"):
        '''
        Retrieves all answers written by given author. The order and limit of answers can be chosen.

        @params
            authorId: The id of the author who has written the answers
            limit, integer (optional): The maximum number of answers retriveved. Default = 10
            order, string (optional): The method for ordering the retrieved answers. "votes" or "latest". Default="latest".
        @example
            /answers/?authorId=123&limit=4&order="votes"
        @perm
            member: All answer information can be given only for members of the organization.
        @return
            200:
                list of retrieved answers
                example: {
                            "answers":[{
                                        "content":"An example answer",
                                        "version":1,
                                        "userId":123,
                                        "created": "2014-01-08T11:05:16",
                                        "modified": "2014-01-08T11:05:16",
                                        "messageId": 4,
                                        "questionId":1,
                                        "accepted":false
                                        }]
                        }
            404: No content found
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }
            400: Bad request, parameters were missing or wrong type
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }
            401: Unauthorized, the user has to be logged in to perform this action
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
            403: Forbidden, the user does not have permission for the action
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
        '''
        messages = []
        if author_id == None:
            messages.append({"content":"A question id has to be provided.","identifier":"questionId"})
        else:
            try:
                if not request.user.is_authenticated():
                    messages.append({"content":"User must be logged in.", "identifier":"user"})
                    return Response({"messages":messages}, 401)
                # Parameter check and default values
                author_id = int(author_id)
                if author_id < 0:
                    raise ValueError("Value is not positive integer")

                if limit == None:
                    limit = 10
                try:
                    limit = int(limit)
                    if limit < 0:
                        raise ValueError("Value is not positive integer")
                except ValueError:
                    messages.append({"content":"The limit has to be a positive integer.","identifier":"limit"})

                if order == None:
                    order = "latest"
                if not order in ["latest","votes"]:
                    messages.append({"content":"The order parameter can be only 'latest' or 'votes'","identifier":"order"})

                if len(messages) == 0:
                    try:
                        author = User.objects.get(user_id=author_id)
                        if not author.organization == request.user.organization:
                            messages.append(compose_message("You are not allowed to perform this action."))
                            return Response({"messages":messages}, 403)
                    except:
                        messages.append({"content":"The author was not found.","identifier":"questionId"})
                        return Response({"messages":messages}, 404)

                    answers = list(Answer.objects.filter(user=author))
                    if len(answers) == 0:
                        messages.append({"content":"The user has not written any answers.","identifier":""})
                        return Response({"messages":messages}, 404)

                    answers = exclude_old_versions(answers)
                    if order == "latest":
                        answers.sort(key=lambda x: x.created)

                    return Response({"answers":[ans.serialize() for ans in answers[:limit]], "messages":messages}, 200)

            except ValueError:
                messages.append({"content":"The author id has to be a positive integer.","identifier":"questionId"})
        return Response({"messages":messages}, 400)
