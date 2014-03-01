# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions as exc

from QnA.models import Question, User, Tag, Keyword
from QnA.serializers import QuestionSerializerGETSingle, QuestionSerializerGETMany, \
                            MessageSerializerPOSTQuestion
from QnA.exceptions import NotFound
from QnA.view_utils import order_messages, get_message_by_id, post_abstract_message


class QuestionAPI(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, rid=None):
        '''
        Retrieves questions according to request parameters (such as question id, author id and tags)
        Functionality can be determined by providing different search parameters and searchInclusion method

        @params
            request: the request parameter from get function
            rid, integer (optional): The id of the question to be retrieved
        @GETparams
            authorId, integer (optional): The id of the author who has written the questions
            authorName, string (optional): The name of the author who has written the questions
            tags, string (optional): tag names separated by comma (eg. "asd1,asd2,asd3")
            tagInclusion, string (optional): The method for selecting the set of required tags. "or" or "and". Default="or".
                @example: lets have tags on, two and three
                    - "and" requires that the retrieved questions have all tags one, two and three
                    - "or" requires that the retrieved questions have one or more of the tags one, two and three
            searchInclusion, string (optional): The method for selecting the set questions retrieved by different searches. "or" or "and". Default="or".
                - "and" requires that the retrieved questions have all same (if provided) author, tags (according to previous setting) and id
                - "or" retrieves all questions found by different search methods
            limit, integer (optional): The maximum number of questions retriveved. Default = 10
            order, string (optional): The method for ordering the retrieved questions. "votes" or "latest". Default="latest".
        @example
            /questions/?authorId=123&limit=4&order=votes
        @perm
            member: All question information can be given only for members of the organization.
        '''
        if rid:
            return self.get_single(request, rid)

        return self.get_many(request)

    def get_single(self, request, rid):

        try:
            question = Question.objects.get(rid=rid)
        except Question.DoesNotExist:
            raise NotFound("Question could not be found.")

        serializer = QuestionSerializerGETSingle(question, context={'user': request.user})

        return Response(serializer.data, 200)

    def get_many(self, request):

        questions = Question.objects.all().order_by('-created')

        if request.GET.get('author_id', None):
            author = User.objects.get(rid=request.GET['author_id'])
            questions.filter(user=author)
        if request.GET.get('limit', None):
            questions = questions[:limit]

        if not questions:
            raise NotFound("No questions could be found.")

        serializer = QuestionSerializerGETMany(questions, many=True)

        return Response({"questions": serializer.data}, 200)

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
                "head": {
                    "title": string
                }
                "content": string,
            }
        @perm
            member: any member can post an question
        '''
        request.DATA['head']['user'] = request.user.pk # important
        request.DATA['user'] = request.user.pk # important

        serializer = MessageSerializerPOSTQuestion(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            question = serializer.object.head
            get_serializer = QuestionSerializerGETSingle(question)
            return Response(get_serializer.data, 201)
        else:
            return Response(serializer.errors, 400)

        raise exc.ParseError("Question could not be created.")

    def put(self, request, rid):
        # todo: add question updating
        pass
