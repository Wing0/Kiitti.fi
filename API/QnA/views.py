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

    if 'content' in data.keys():
        abstractmessage.content = data["content"]
    else:
        abstractmessage.content = ""

    if 'version' in data.keys():
        abstractmessage.version = data["version"]
    else:
        abstractmessage.version = -1

    if 'userId' in data.keys():

        abstractmessage.user = User.objects.get(user_id=data["userId"])
    else:
        raise Exception("You must provide valid user id.")
    '''
    if 'messageId' in data.keys():
        abstractmessage.message_id = data["messageId"]
    else:
        raise Exception("You must provide valid message id.")
    '''


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
            abs_data.save()
            # Save tags
            taglist = data.get("tags")
            if taglist and isinstance(taglist,list):
                for tagname in list(set(taglist)):
                    try:
                        tag = Tag.objects.get(name=tagname)
                        entry = TagEntry(tag=tag, message_id=abs_data.message_id, creator=abs_data.user)
                        entry.save()
                    except:
                        messages.append({"type": "alert", "content": "Tag %s was not found." % tag, "identifier": "tags"})
                        # Create tag?

        return Response({"messages":messages},200)

    def get(self, request, style="hottest"):
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

        amount = request.GET.get("amount")
        if not amount:
            amount = 10
        tags = request.GET.get("tags")
        if not tags:
            tags = []
        else:
            tags = json.loads(tags)
        print tags
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
            questions = Question.objects.all()

        question_data = []
        questions = [q for q in questions]
        if style == "latest":
            questions.sort(key = lambda a: a.created)# - b.created).seconds)
        elif style == "hottest":
            questions.sort(key = lambda a: sum([vote.rate for vote in Vote.objects.filter(message_id=a.message_id)]))# - sum([vote.rate for vote in Vote.objects.filter(message_id=b.message_id)]))
        print questions, amount
        questions = questions[:int(amount)]
        for question in questions:
            question_data.append(question.serialize())

        return Response({"questions": question_data}, 200)

class TagAPI(APIView):

    def post(self, request):
        success = False
        data = json.loads(request.body)

        # Input validation
        valid_input = True
        messages = []
        organization_id = data.get("organizationId")
        if organization_id == None:
            valid_input = False
            messages.append({"type": "alert", "content": "Organization id is missing.", "identifier": "organizationId"})
        else:
            if isinstance(organization_id, int):
                try:
                    organization = Organization.objects.get(organization_id = organization_id)
                except:
                    messages.append({"type": "alert", "content": "Organization id did not match any organization.", "identifier": "organizationId"})
            else:
                messages.append({"type": "alert", "content": "Organization id must be a positive integer.", "identifier": "organizationId"})
        name = data.get("name")
        if not name:
            valid_input = False
            messages.append({"type": "alert", "content": "Tag name is missing.", "identifier": "name"})
        course_flag =  data.get("courseFlag")
        if not course_flag in [True, False]:
            valid_input = False
            messages.append({"type": "alert", "content": "Coursee flag information is missing.", "identifier": "courseFlag"})
        user_id = data.get("userId")
        if user_id == None:
            if request.user.is_authenticated():
                user = request.user
            else:
                valid_input = False
                messages.append({"type": "alert", "content": "Please log in or provide user id.", "identifier": "userId"})
        else:
            try:
                user = User.objects.get(user_id=user_id)
            except:
                valid_input = False
                messages.append({"type": "alert", "content": "Provided user id does not match any user.", "identifier": "userId"})

        # Model creation
        if valid_input:
            tag = Tag(organization=organization, course_flag=course_flag, name = name, creator=user)

            # Model data validation
            valid, messages = tag.validate(messages)
            if valid:
                tag.save()
                success = True

        return Response({"messages":messages, "success":success},200)

    def get(self, request):
        '''
        Tags can be searched by id, by creator id or one can fetch a number tags.
        One can also specify certain amount to be fetch (sorted by date or number of tag entries)
        input parameters and format:
        tagId: Positive integer, get a tag by this id
        userId: Positive integer, get tags created by corresponding user
        amount: Positive integer, resterict the number of tags returned, default = 10
        order: String, "date" or "entries", ordering method

        '''
        amount = 10
        order_method = "date"
        # Validate input
        messages = []
        data = []
        if request.GET.get("tagId"):
            try:
                data.append(Tag.objects.get(tag_id=request.GET.get("tagId")).serialize())
            except:
                messages.append({"type": "alert", "content": "Tag id is not valid.", "identifier": "tagId"})
        else:
            tmp_amount = request.GET.get("amount")
            if tmp_amount:
                if isinstance(tmp_amount, int) and tmp_amount > 0:
                    amount = tmp_amount
                else:
                    messages.append({"type": "alert", "content": "Amount must a positive integer.", "identifier": "amount"})
            tmp_order_method = request.GET.get("order")
            if tmp_order_method:
                if tmp_order_method in ["created","entries"]:
                    order_method = tmp_order_method
                else:
                    messages.append({"type": "alert", "content": "Tags can only be ordered by date created and number of entries.", "identifier": "amount"})
            user_id = request.GET.get("userId")
            if user_id:
                if isinstance(user_id, int):
                    user = False
                    try:
                        user = User.objects.get(user_id = user_id)
                    except:
                        messages.append({"type": "alert", "content": "The user id does not match any user.", "identifier": "userId"})
                    if user:
                        if order_method == "created":
                            tags = Tag.objects.filter(creator = user).order_by("created")[:amount]
                        else:
                            tags = Tag.objects.filter(creator = user)
                            tags = sorted(tags, key = lambda tag: len(TagEntry.objects.filter(tag=tag)))[:amount]
                        data = [tag.serialize() for tag in tags]
                else:
                    messages.append({"type": "alert","content": "User id has to be a positive integer","identifier": "userId"})
            else:
                if order_method == "created":
                    tags = Tag.objects.all().order_by("created")[:amount]
                else:
                    tags = Tag.objects.all()
                    tags = sorted(tags, key = lambda tag: len(TagEntry.objects.filter(tag=tag)))[:amount]
                data = [tag.serialize() for tag in tags]
        return Response({"tags": data, "messages":messages}, 200)

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


