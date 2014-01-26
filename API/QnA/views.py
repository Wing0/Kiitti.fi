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


class UserAPI(APIView):

    def get(self, request):
        return Response({"users": get_user_data()}, 200)

    #VALIDATE
    def post(self, request):
        data = json.loads(request.body)
        if ("username" in data
            and "email" in data
            and "firstName" in data
            and "lastName" in data
            and "organizationId" in data
            and "password" in data):

            user = User(username=data["username"],
                        email=data["email"],
                        first_name=data["firstName"],
                        last_name=data["lastName"],
                        organization_id=data["organizationId"],
                        password=data["password"])

            valid, messages = user.validate()
            if valid:
                user.set_password(user.password)
                try :
                    user.save()
                except IntegrityError, e:
                    valid = False
                    if e.message == "column username is not unique":
                        messages.append({"type":"alert", "content": "Username already in use.", "identifier":"username"})
                    else:
                        messages.append({"type":"alert", "content": e.message, "identifier":""})
        else:
            messages = [{"type":"Alert","content":"Something is missing","identifier":""}]
            valid = False
        return Response({"messages":messages},200)

class VoteAPI(APIView):

    def get(self, request):
        data = []
        votedata = Vote.objects.all()
        for vote in votedata:
            data.append(vote.serialize())
        return Response({"votes": data}, 200)

    def post(self, request):
        data = json.loads(request.body)
        vote = Vote()
        if 'rate' in data:
            vote.rate = data["rate"]
        else:
            rate = 0
        if 'userId' in data:
            vote.user_id = data["userId"]
        else:
            return Response({"messages": {
                "type": "alert",
                "content": "User id has to be a positive integer",
                "identifier": "user_id"}}, 200)
        if 'messageId' in data:
            vote.message_id = data["messageId"]
        else:
            return Response({"messages": {
                "type": "alert",
                "content": "Message id has to be a positive integer",
                "identifier": "message_id"}}, 200)
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
        messages = {}
        try:
            abs_data = post_abstract_message(Answer(), data)
        except Exception, e:
            return Response({"messages": {"type": "alert", "content": str(e), "identifier": ""}}, 200)

        if 'accepted' in data:
            abs_data.accepted = data["accepted"]
        else:
            abs_data.accepted = False
        if 'questionId' in data:
            abs_data.question_id = data["questionId"]
        else:
            abs_data.question_id = None
        valid, messages = abs_data.validate()
        if valid:
            abs_data.save()
        return Response({"messages": messages}, 200)

class CommentAPI(APIView):

    def post(self, request):
        data = json.loads(request.body)
        messages = {}
        try:
            abs_data = post_abstract_message(Comment(), data)
        except Exception, e:
            return Response({"messages": {"type": "alert", "content": str(e), "identifier": ""}}, 200)

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

        if not "userId" in data and request.user.is_authenticated():
            data["userId"] = request.user.user_id
        messages = {}
        try:
            abs_data = post_abstract_message(Question(), data)
        except Exception, e:
            messages = {"type": "alert", "content": str(e), "identifier": ""}
            return Response({"messages": messages}, 200)
        title = data.get('title')
        abs_data.title = title

        valid, messages = abs_data.validate()
        if valid:
            if abs_data.message_id:
                abs_data.save_changes()
            else:
                abs_data.save()
            # Save tags
            taglist = data.get("tags")
            if taglist and isinstance(taglist,list):
                existing_tags = [tag_entry.tag.name for tag_entry in TagEntry.objects.filter(message_id=abs_data.message_id)]

                for tagname in [tag for tag in list(set(taglist)) if tag not in existing_tags]:
                    try:
                        tag = Tag.objects.get(name=tagname)
                        entry = TagEntry(tag=tag, message_id=abs_data.message_id, creator=abs_data.user)
                        entry.save()
                    except:
                        messages.append({"type": "alert", "content": "Tag %s was not found." % tag, "identifier": "tags"})
                        # Create tag?

        return Response({"messages":messages},200)

    def get(self, request, criterion="latest"):
        '''
            Questions can be searched in three different ways:
            1. By messageId:
                required parameters:
                    messageId, positive integer
                returns:
                    All questions matchin with given messageId ordered by descending version number
            2. By tags:
                required parameters:
                    tags: list of tag names
                optional parameters:
                    criterion: latest or hottest, sort objects by date or votes
                    amount: maximum number of objects returned
                        default=10
                    searchMethod: 'or' or 'and', defines whether the returned question set is union or intersection of given tags
                        default='and'
                returns: Specified amount of latest versions of questions including the given tags sorted by given criterion
            3. By votes or date:
                optional parameters:
                    criterion: latest or hottest, sort objects by date or votes
                    amount: maximum number of objects returned
                        default=10
                returns: Specified amount of latest versions of questions sorted by given criterion
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

        if request.GET.get("messageId"):
            question_data =[]
            message_id = request.GET.get("messageId")
            if isinstance(message_id, int), and message_id >= 0:
                try:
                    Question.objects.filter(message_id=message_id).order_by("-version")
                except:
                    pass
            return Response({"questions": question_data}, 200)

        amount = request.GET.get("amount")
        if not amount:
            amount = 10
        tags = request.GET.get("tags")
        if not tags:
            tags = []
        else:
            tags = json.loads(tags)
        if len(tags):
            search_method = "or"
            # Filter tags of invalid form
            tags = [tag for tag in tags if tag and isinstance(tag, basestring)]

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
                    for ind, subset in question_sets:
                        if ind == 0:
                            continue
                        questions = intersect(questions, subset)
        else:
            # Get all questions sorted by version
            tmp_questions = list(Question.objects.all())
            tmp_questions.sort(key=lambda q: -q.version)

            used = []
            questions = []
            # Append first occurrence of message id to questions
            for q in tmp_questions:
                if q.message_id not in used:
                    questions.append(q)
                    used.append(q.message_id)

        question_data = []
        questions = [q for q in questions]
        if criterion == "latest":
            questions.sort(key = lambda a: a.created, reverse=True)# - b.created).seconds)
        elif criterion == "hottest":
            questions.sort(key = lambda a: sum([vote.rate for vote in Vote.objects.filter(message_id=a.message_id)]))# - sum([vote.rate for vote in Vote.objects.filter(message_id=b.message_id)]))
        questions = questions[:int(amount)]
        for question in questions:
            question_data.append(question.serialize())

        return Response({"questions": question_data}, 200)


class OrganizationAPI(APIView):

    def get(self, request):
        data = Organization.objects.all()
        data = [obj.serialize() for obj in data]
        return Response({"organizations": data}, 200)

    def post(self, request):
        success = False
        messages = []
        data = json.loads(request.body)
        valid_input = True
        if not data.get("name"):
            messages.append({"type": "alert","content": "Organization name must be provided.","identifier": "name"})
            valid_input = False
        if not data.get("address"):
            messages.append({"type": "alert","content": "Organization address must be provided.","identifier": "address"})
            valid_input = False
        if valid_input:
            org = Organization(name=data.get("name"), address=data.get("address"))
            valid, messages = org.validate()
            if valid:
                org.save()
                success = True
        return Response({"messages":messages, "success":success}, 200)


