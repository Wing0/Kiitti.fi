from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import *
import json



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


    if 'messageId' in data.keys():
        abstractmessage.message_id = data["messageId"]

    if 'content' in data.keys():
        abstractmessage.content = data["content"]
    else:
        abstractmessage.content = ""

    if 'userId' in data.keys():
        abstractmessage.user = User.objects.get(user_id=data["userId"])
    else:
        raise Exception("You must provide valid user id.")



    return abstractmessage












