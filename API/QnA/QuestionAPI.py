from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import *
from QnA.view_utils import *
from QnA.utils import *
import json

class QuestionAPI(APIView):

    def post(self, request):
        '''
        This method saves new question into database
        @params (this means body parameters, not autoinserted by django)
            version, positive integer: version number of the question.
            title, string: title of the Question
            content, string: content text of the Question
            messageId, positive integer: message id of the Question. For client: set this only if you are updating old message. save() method
            will give new messageId for new messages!
        @example:
            {
                "version":1,
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

        data = json.loads(request.body)


        messages = []

        if not request.user.is_authenticated():
            messages.append(compose_message("User must be logged in.", "user"))
            return Response({"messages":messages}, 401)


        abs_data = post_abstract_message(Question(), data)


        title = data.get('title')
        abs_data.title = title
        abs_data.organization = request.user.organization
        abs_data.user = request.user
        valid, messages = abs_data.validate()
        if valid:
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
                        messages.append(compose_message("Tag %s was not found." % tagname, "tags"))
            if len(messages) == 0:
                if abs_data.message_id:
                    abs_data.save_changes()
                else:
                    abs_data.save()
                return Response({"messages": messages}, 201)

        return Response({"messages":messages},400)

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
            if isinstance(message_id, int) and message_id >= 0:
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
