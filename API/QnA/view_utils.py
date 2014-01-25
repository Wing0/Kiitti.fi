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

def get_message_by_id(msgtype, msgid):
    '''
    Get message by id.

    @params
        msgtype: Name of abstractmessage class as string. Example: "Question".
        msgid, int: Organization id which should be returned.
    @example
        /questions/?messageId=223
    @perm
        member: Get message.
    @return
        200: Found organization.
            example:
            {
                "comment":[
                    {
                        "content":"I am content of message.",
                        "created":"01.01.2014 16:33:41",
                        "modified":"15.01.2014 08:10:22",
                        "version": ,
                        "user": {
                                    "name": "Wingo",
                                    ....
                                }
                    }
                ]
            }
        204: No content found. List of appropriate error messages.
            example:
            {
                "messages":[{"content":"An example error message.","identifier":"example"}]
            }
        400: Invalid parameters. List of appropriate error messages.
            example:
            {
                "messages":[{"content":"An example error message.","identifier":"example"}]
            }
    '''
    if not isinstance(msgid, int):
        return Response({"messages":[{"content":"Message id must be integer.","identifier":"msgid"}]}, 400)
    if not isinstance(msgtype, basestring):
        return Response({"messages":[{"content":"Model must be exact classname.","identifier":"msgtype"}]}, 400)
    if msgtype == "Comment":
        try:
            return Response({"comments": Comment.objects.get(message_id=msgid).serialize()}, 200)
        except:
            return Response({"messages":[{"content":"No comments with given id.","identifier":"msgid"}]}, 204)
    elif msgtype == "Answer":
        try:
            return Response({"answers": Answer.objects.get(message_id=msgid).serialize()}, 200)
        except:
            return Response({"messages":[{"content":"No answers with given id.","identifier":"msgid"}]}, 204)
    elif msgtype == "Question":
        try:
            return Response({"questions": Question.objects.get(message_id=msgid).serialize()}, 200)
        except:
            return Response({"messages":[{"content":"No questions with given id.","identifier":"msgid"}]}, 204)
    else:
        return Response({"messages":[{"content":"Invalid message classname.","identifier":"msgtype"}]}, 400)


def post_abstract_message(abstractmessage, data):
    '''
    Sets the values of given abstractmessage instance equal to datas' values.

    @params
        abstractmessage, AbstractMessage: Instance of class that subclasses AbstractMessage.
        data, JSON-dictionary: Is array that contains all json data.
    @return Given instance of abstractmessage populated with data in given dictionary.
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












