from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from QnA.models import *
from QnA.view_utils import order_messages, get_message_by_id, post_abstract_message
from QnA.utils import *
import json

class QuestionAPI(APIView):

    def post(self, request):
        '''
        This method saves new question into database
        @params (this means body parameters, not autoinserted by django or other methods)
            title, string: title of the Question
            content, string: content text of the Question
            messageId, positive integer: message id of the Question. For client: set this only if you are updating old message. save() method
            will give new messageId for new messages!
        @example:
            {
                "title": "Why does the sun go down every night?",
                "content":"Why does the sun go down every night? I don't understand!",
                "messageId":3,
                "tags": ["tagFirst", "tagSecond"]
            }
        @perm
            member: any member can post an question
        @return
            201: Created, the question was succesfully created
            400: Bad request, parameters were missing or wrong type
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }
            401: Unauthorized, the user has to be loggend in to perform this action
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
        '''

        messages = []

        if not request.user.is_authenticated():
            messages.append(compose_message("User must be logged in.", "user"))
            return Response({"messages":messages}, 401)

        question = post_abstract_message(Question(), request.DATA)

        title = request.DATA.get('title')
        question.title = title
        question.organization = request.user.organization
        question.user = request.user
        messages = question.validate()
        if len(messages) == 0:

            # Save question
            if question.message_id:
                question.save_changes()
            else:
                question.save()

            # Save tags
            taglist = request.DATA.get("tags")
            if taglist and isinstance(taglist,list):
                tagnames = list(set(taglist)) #List(set()) removes duplicates
                for tagname in tagnames:
                    try:
                        tag = Tag.objects.get(name=tagname)
                        entry = TagEntry(tag=tag, message_id=question.message_id, creator=question.user)
                        entry.save()
                    except:
                        messages.append(compose_message("Tag %s was not found." % tagname, "tags"))
            return Response(create_message("success", "question_post"), 201)

        return Response({"messages":messages},400)

    def get(self, request, criterion="latest"):
        '''
        This method mediates the task to correct function.
        Further information in helper method docstring
        '''

        if not request.user.is_authenticated():
            return Response({"messages":create_message("User must be logged in.")}, 401)

        if request.GET.get("authorId") != None:
            return self.by_author(request, request.GET.get("authorId"), request.GET.get("limit"), request.GET.get("order"))
        elif request.GET.get("tags"):
            return self.by_tags(request, request.GET.get("tags"), request.GET.get("searchMethod"), request.GET.get("limit"), request.GET.get("order"))
        elif request.GET.get("questionId") != None:
            return self.by_id(request, request.GET.get("questionId"), request.GET.get("order"), request.GET.get("history"))
        else:
            return self.get_all(request, request.GET.get("limit"), request.GET.get("order"))


    def by_author(self, request, author_id, limit=10, order="latest"):
        '''
        Retrieves all questions written by given author. The order and limit of questions can be chosen.

        @params
            request: the request parameter from get function
            author_id: The id of the author who has written the questions
            limit, integer (optional): The maximum number of questions retriveved. Default = 10
            order, string (optional): The method for ordering the retrieved questions. "votes" or "latest". Default="latest".
        @example
            /questions/?authorId=123&limit=4&order=votes
        @perm
            member: All question information can be given only for members of the organization.
        @return
            200:
                list of retrieved questions
                example: {
                            "questions":[{
                                        "title":"What is the question?",
                                        "content":"An example question",
                                        "version":1,
                                        "userId":123,
                                        "created": "2014-01-08T11:05:16",
                                        "modified": "2014-01-08T11:05:16",
                                        "messageId": 4,
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
            messages.append({"content":"A author id has to be provided.","identifier":"authorId"})
        else:
            try:
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
                        messages.append({"content":"The author was not found.","identifier":"authorId"})
                        return Response({"messages":messages}, 404)

                    questions = list(Question.objects.filter(user=author))
                    if len(questions) == 0:
                        messages.append({"content":"The user has not written any questions.","identifier":""})
                        return Response({"messages":messages}, 404)

                    questions = exclude_old_versions(questions)
                    questions = order_messages(questions, order)

                    question_data = []

                    for q in questions[:limit]:
                        json = q.serialize()
                        question_data.append(json)

                    return Response({"questions":question_data, "messages":messages}, 200)

            except ValueError:
                messages.append({"content":"The author id has to be a positive integer.","identifier":"authorId"})
        return Response({"messages":messages}, 400)

    def by_tags(self, request, tags, search_method = "or", limit=10, order="latest"):
        '''
        Retrieves all questions that include one of the tags or all given tags depending on search method.

        @params
            request: the request parameter from get function
            tags, string: tag names separated by comma (eg. "asd1,asd2,asd3")
            search_method, string: The method for selecting the set of required tags. "or" or "and". Default="or".
                @example: lets have tags on, two and three
                    - "and" requires that the retrieved questions have all tags one, two and three
                    - "or" requires that the retrieved questions have one or more of the tags one, two and three
            limit, integer (optional): The maximum number of questions retriveved. Default = 10
            order, string (optional): The method for ordering the retrieved questions. "votes" or "latest". Default="latest".
        @example
            /questions/?tags=one,two,three&searchMethod=and&limit=5&order=latest
        @perm
            member: All question information can be given only for members of the organization.
        @return
            200:
                list of retrieved questions
                example: {
                            "questions":[{
                                        "title":"What is the question?",
                                        "content":"An example question",
                                        "version":1,
                                        "userId":123,
                                        "created": "2014-01-08T11:05:16",
                                        "modified": "2014-01-08T11:05:16",
                                        "messageId": 4,
                                        },{...},{...}]
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
        '''
        # Helping methods for the tag search
        def unique(a):
            """ return the list with duplicate elements removed """
            return list(set(a))

        def intersect(a, b):
            """ return the intersection of two lists """
            return list(set(a) & set(b))

        def union(a, b):
            """ return the union of two lists """
            return list(set(a) | set(b))

        messages = []

        # Parameter check and default values
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

        if search_method == None:
            search_method = "or"
        if not search_method in ["or","and"]:
            messages.append({"content":"The search method parameter can be only 'or' or 'and'","identifier":"searchMethod"})

        tags = request.GET.get("tags").split(",")
        tags = [tag for tag in tags if tag and isinstance(tag, basestring)]

        if not len(tags):
            messages.append({"content":"One or more valid tags required.", "identifier":"tags"})
            return Response({"messages":messages}, 400)
            # Filter tags of invalid form
        else:
            questions = []
            question_sets = [[] for tag in tags]    # Lists of questions corresponding each tag in the same order
            for ind, tag in enumerate(tags):
                # Get all tag entries for the tag
                try:
                    tag_entries = Tag.objects.get(name=tag).tagentry_set.all()
                except:
                    tag_entries = []
                # Fetch all questions corresponding the tag entries
                for tag_entry in tag_entries:
                    try:
                        question = Question.objects.filter(message_id=tag_entry.message_id).order_by('-version')[0]
                        if question:
                            question_sets[ind].append(question)
                    except:
                        pass

            if search_method == "or":
                questions = unique([q for subset in question_sets for q in subset])
            elif search_method == "and":
                if len(question_sets) == 1:
                    questions = question_sets[0]
                else:
                    questions = question_sets[0]
                    for ind, subset in enumerate(question_sets):
                        if ind == 0:
                            continue
                        questions = intersect(questions, subset)
        if not len(questions):
            messages.append({"content":"No questions found for this query.", "identifier":""})
            return Response({"messages":messages}, 404)
        questions = exclude_old_versions(questions)
        questions = order_messages(questions, order)

        question_data = [q.serialize() for q in questions[:limit]]

        return Response({"questions": question_data}, 200)

    def by_id(self, request, question_id, order="latest", history=False):
        '''
        Retrieves the question and question history matching the given question id.
        The order is for the answers.

        @params
            request: the request parameter from get function
            question_id: The message_id of the question
            order, string (optional): The method for ordering the retrieved answers for the question. "votes" or "latest". Default="latest".
        @example
            /questions/?questionId=123&order=votes
        @perm
            member: All question information can be given only for members of the organization.
        @return
            200:
                list of retrieved questions
                example: {
                            "question":{
                                        "title":"What is the question?",
                                        "content":"An example question",
                                        "version":1,
                                        "userId":123,
                                        "created": "2014-01-08T11:05:16",
                                        "modified": "2014-01-08T11:05:16",
                                        "messageId": 4,
                                        },

                            "answers":[{
                                        "content":"An example answer",
                                        "version":1,
                                        "userId":123,
                                        "created": "2014-01-08T11:05:16",
                                        "modified": "2014-01-08T11:05:16",
                                        "messageId": 4,
                                        "questionId":1,
                                        "accepted":false
                                        }, {...}, {...}]
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
            messages.append({"content":"A question id must be provided.","identifier":"questionId"})
        else:
            try:
                # Parameter check and default values
                question_id = int(question_id)
                if question_id < 0:
                    raise ValueError("Value is not positive integer")

                if order == None:
                    order = "latest"
                if not order in ["latest","votes"]:
                    messages.append({"content":"The order parameter can be only 'latest' or 'votes'","identifier":"order"})

                if len(messages) == 0:
                    try:
                        questions = list(Question.objects.filter(message_id=question_id).order_by("-version"))
                        question = exclude_old_versions(questions)[0]
                        if not question.organization == request.user.organization:
                            messages.append(compose_message("You are not allowed to perform this action."))
                            return Response({"messages":messages}, 403)
                    except:
                        messages.append({"content":"The question was not found.","identifier":"questionId"})
                        return Response({"messages":messages}, 404)


                    answers = self.get_answers(question, order)


                    questions = [q.serialize() for q in questions]
                    if history:
                        return Response({"questions":questions, "answers":answers,"messages":messages}, 200)
                    else:
                        return Response({"questions":questions[0], "answers":answers, "messages":messages}, 200)

            except ValueError:
                messages.append({"content":"The question id has to be a positive integer.","identifier":"questionId"})
        return Response({"messages":messages}, 400)


    def get_all(self, request, limit=10, order="latest"):
        '''
        Retrieves all questions that include one of the tags or all given tags depending on search method.

        @params
            request: the request parameter from get function
            limit, integer (optional): The maximum number of questions retriveved. Default = 10
            order, string (optional): The method for ordering the retrieved questions. "votes" or "latest". Default="latest".
            get_answers, boolean (optional): If this is True, the function will return serialized answers with
        @example
            /questions/?limit=5&order=latest
        @perm
            member: All question information can be given only for members of the organization.
        @return
            200:
                list of retrieved questions
                example: {
                            "questions":[{
                                        "title":"What is the question?",
                                        "content":"An example question",
                                        "version":1,
                                        "userId":123,
                                        "created": "2014-01-08T11:05:16",
                                        "modified": "2014-01-08T11:05:16",
                                        "messageId": 4,
                                        },{...},{...}]
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
        '''
        messages = []
        # Parameter check and default values

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
            #questions = Question.objects.all()
            questions = list(Question.objects.filter(organization=request.user.organization.organization_id))
            if len(questions) == 0:
                messages.append({"content":"There are no questions in the organization.","identifier":""})
                return Response({"messages":messages}, 404)

            #print questions
            questions = exclude_old_versions(questions)
            questions = order_messages(questions, order)

            question_data = [q.serialize() for q in questions[:limit]]

            return Response({"questions":question_data, "messages":messages}, 200)

        return Response({"messages":messages}, 400)

    def get_answers(self, question, order=False):
        answers = list(Answer.objects.filter(question_id=question.message_id))
        if order:
            answers = order_messages(answers, order)
        return [ans.serialize() for ans in exclude_old_versions(answers)]

