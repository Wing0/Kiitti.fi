from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import User, Vote, AbstractMessage, Comment, Answer
import json
import re

# Create your views here...


def get_user_data():
    data = []
    userdata = User.objects.all()
    for user in userdata:
        data.append(user.serialize())
    return data

def get_question(time):
    data = []
    questiondata = Question.objects.filter(date__gte=time)
    for question in questiondata:
        data.append(question.serialize())
    return data

def post_abstract_message(abstractmessage, data):
    '''
    abstractmessage must be an instance of class that subclasses AbstractMessage.
    data is array that contains all json data.
    '''
    content = data["content"]
    version = data["version"]
    user_id = data["userId"]
    created = data["created"]
    modified = data["modified"]
    message_id = data["messageId"]

    abstractmessage.content = content
    abstractmessage.version = version
    abstractmessage.user_id = user_id
    abstractmessage.created = created
    abstractmessage.modified = modified
    abstractmessage.message_id = message_id
    return abstractmessage

class UserAPI(APIView):

    def get(self, request):
        return Response({"users": get_user_data()}, 200)

    #VALIDATE
    def post(self, request):
        data = json.loads(request.body)

        user = User(username=data["username"], email=data["email"], first_name=data["first_name"], last_name=data["last_name"])
        valid, messages = user.validate()
        if valid:
            user.save()
        return Response({"messages":messages, "valid":valid},200)

class VoteAPI(APIView):

    def get(self, request):
        data = []
        votedata = Vote.objects.all()
        for vote in votedata:
            data.append(vote.serialize())
        return Response({"votes": data}, 200)

    def post(self, request):
        data = json.loads(request.body)
        vote_value = data['vote']
        user_id = data['userId']
        message_id = data['messageId']
        rate = data['rate']
        vote = Vote()
        vote.type = vote_value
        vote.user_id = user_id
        vote.message_id = message_id
        vote.rate = rate
        vote.save()
        return Response(200)

class AnswerAPI(APIView):

    def get(self, request):
        data = []
        answer_data = Answer.objects.all()
        for answer in answer_data:
            data.append(answer.serialize())
        return Response({"answers": data}, 200)

    def post(self, request):
        data = json.loads(request.body)

        abs_data = post_abstract_message(Answer(), data)
        accepted = data["accepted"]
        question_id = data["questionId"]
        abs_data.accepted = accepted
        abs_data.question_id = question_id
        abs_data.save()

        return Response(200)

class CommentAPI(APIView):

    def post(self, request):
        data = json.loads(request.body)
        abs_data = post_abstract_message(Comment(), data)

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

class QuestionAPI(APIView):

    def post(self, request):
        data = json.loads(request.body)
        abs_data = post_abstract_message(Question(), data)
        topic = data['topic']
        abs_data.topic = topic
        abs_data.save()
        return Response(200)

