from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import *
import json

def exclude_old_versions(message_list):
    # Sort all messages by version
    tmp_questions.sort(key=lambda q: -q.version)

    used = []
    messages = []
    # Append first occurrence of message id to messages
    for q in tmp_questions:
        if q.message_id not in used:
            messages.append(q)
            used.append(q.message_id)
    return messages

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

def get_message_by_id(model, msgid):
    '''
    Get message by id.

    @params
        model: Subclass of abstractmessage class as string. Example: Question.
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
    #if not isinstance(model, AbstractMessage):
    #   return Response({"messages":[{"content":"Model must be class that subclasses abstractmessage.","identifier":"model"}]}, 400)
    name = "%ss" %model.__name__.lower()
    try:
        data = []
        messagedata = model.objects.filter(message_id=msgid)
        for message in messagedata:
            data.append(message.serialize())
        return Response({name: data}, 200)
    except:
        return Response({"messages":[{"content":"No " + name + " with given id.","identifier":"msgid"}]}, 204)


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
    return abstractmessage
