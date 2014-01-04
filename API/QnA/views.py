from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import User, Vote, AbstractMessage
import json

# Create your views here...

PARAMETERS = (
"time": 86400,
"amount": 10,
"keyword": "",
"tag": "",
"creator": ""
)

def get_user_data(self):
    data = []
    userdata = User.objects.all()
    for user in userdata:
        data.append(user.serialize.())
    return data

def get_question(self, time):
    data = []
    questiondata = Question.objects.filter(date__gte=time)
    for question in questiondata:
        data.append(question.serialize.())
    return data

def get_abstract_message(self, parameters):


def create_message(self, abstractmessage, data):
    '''
    abstractmessage must be an instance of class that subclasses AbstractMessage.
    data is array that contains all json data.
    '''
    content = data["content"]
    version = data["version"]
    user_id = data["user_id"]
    created = data["created"]
    modified = data["modified"]
    message_id = data["message_id"]

    abstractmessage.content = content
    abstractmessage.version = version
    abstractmessage.user_id = user_id
    abstractmessage.created = created
    abstractmessage.modified = modified
    abstractmessage.message_id = message_id
    return abstractmessage

class UserAPI(APIView):

    def get(self, request):
        return Response({"users": get_user_data(request.GET)}, 200)

    #VALIDATE
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        user_id = data['user_id']
        reputation = data['reputation']
        user = User()
        user.username = username
        user.user_id = user_id
        user.reputation = reputation
        user.save()
        return Response(200)

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
        user_id = data['user_id']
        message_id = data['message_id']
        vote = Vote()
        vote.type = vote_value
        vote.user_id = user_id
        vote.message_id = message_id
        return Response(200)

class AnswerAPI(APIView):

    def post(APIView):
        data = json.loads(request.body)
        absdata = create_message(Answer(), data)

        accepted = data["accepted"]
        question_id = data["question_id"]
        absdata.accepted = accepted
        absdata.question_id = question_id
        return Response(200)

