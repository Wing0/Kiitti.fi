from rest_framework.response import Response

from QnA.models import *  # todo: clean this import


def order_messages(msg_list, order):
    if not order in ["latest", "votes"]:
        raise ValueError("Invalid order value")
    if order == "latest":
        msg_list.sort(key=lambda x: x.created, reverse=True)
    elif order == "votes":
        # questions.sort(key = lambda a: sum([vote.rate for vote in
        # Vote.objects.filter(message_id=a.message_id)]))# - sum([vote.rate for
        # vote in Vote.objects.filter(message_id=b.message_id)]))
        pass

    return msg_list


def get_message_by_id(model, msgid, organization, history=False):
    '''
    Get message by id.

    @params
        model, AbstractMessage: Subclass of abstractmessage class. Example: Question.
        msgid, int: Message id which should be returned.
        organization, int: Organization id where user belongs.
        history, boolean: If true includes version history, else latest message is returned.
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
        400: Invalid parameters. List of appropriate error messages.
            example:
            {
                "messages":[{"content":"An example error message.","identifier":"example"}]
            }
    '''
    messages = []
    if model is None:
        messages.append(compose_message("No model type provided.", "model"))
    if not isinstance(msgid, int) or msgid < 0:
        messages.append(
            compose_message("Message id must be positive integer.", "msgid"))
    if not isinstance(history, bool):
        messages.append(
            compose_message("History must be boolean value.", "history"))
    # if not isinstance(model, AbstractMessage):
    # return Response({"messages":[{"content":"Model must be class that
    # subclasses abstractmessage.","identifier":"model"}]}, 400)
    if len(messages) == 0:
        name = "%ss" % model.__name__.lower()
        try:
            data = []
            messagedata = model.objects.filter(message_id=msgid)
            if len(messagedata) > 0 and messagedata[0].organization.organization_id != organization:
                return Response(create_message("You are not allowed to perform this action."), 403)
            for message in messagedata:
                data.append(message.serialize())
            if history:
                return Response({name: data}, 200)
            else:
                length = len(data)
                return Response({name: data[length - 1].serialize()}, 200)
        except:
            messages.append(compose_message("Message id not found.", "msgid"))

    return Response({"messages": messages}, 400)


def post_abstract_message(abstractmessage, data):
    '''
    Sets the values of given abstractmessage instance equal to datas' values.

    @params
        abstractmessage, AbstractMessage: Instance of class that subclasses AbstractMessage.
        data, dictionary: Is array that contains all data in request body.
    @return Given instance of abstractmessage populated with data in given dictionary.
    '''

    if 'messageId' in data.keys():
        abstractmessage.message_id = data["messageId"]
    if 'version' in data.keys():
        abstractmessage.version = data["version"]
    if 'content' in data.keys():
        abstractmessage.content = data["content"]
    else:
        abstractmessage.content = ""
    return abstractmessage


def serialize_answers(answers):
    '''
    Serializes given array filled with Answer objects.
    Adds serialized comments also.

    @params
        answers, array: List of answers to serialize.
    @return
        List of serialized answers.
    '''
    answer_list = []
    for ans in answers:
        json = ans.serialize()
        comments = Comment.objects.filter(parent_id=ans.message_id)
        comment_list = []
        for comment in comments:
            comment_list.append(comment.serialize())
        json["comments"] = comment_list
        answer_list.append(json)

    return answer_list
