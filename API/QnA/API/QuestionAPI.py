from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from QnA.models import Question, User, Tag, TagEntry
from QnA.view_utils import order_messages, get_message_by_id, post_abstract_message
from QnA.utils import compose_message, create_message, exclude_old_versions, intersect, unique
import json

class QuestionAPI(APIView):
    permission_classes = (IsAuthenticated,)

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

        messages = []

        if not request.user.is_authenticated():
            messages.append(compose_message("User must be logged in.", "user"))
            return Response({"messages":messages}, 401)

        question = post_abstract_message(Question(), request.DATA)

        title = request.DATA.get('title')
        question.title = title
        question.organization = request.user.organization
        question.user = request.user
        messages = question.validate()
        if len(messages) == 0:

            # Save edited question
            if question.message_id:
                parent_question = Question.objects.filter(message_id=question.message_id).order_by("-version")[0]
                question.save_changes()
            else:
                # Confirm uniqueness of the title within the organization before saving
                try:
                    Question.objects.get(title=question.title, organization=question.organization)
                    return Response(create_message("The title is in use"), 400)
                except:
                    question.save()

            # Save tags
            taglist = request.DATA.get("tags")
            if taglist and isinstance(taglist,list):
                taglist = unique(taglist) #List(set()) removes duplicates
                # Delete existing tags
                previous_taglist = TagEntry.objects.filter(message_id=question.message_id)
                taglist = [tag for tag in taglist if tag not in previous_taglist]
                for tag in previous_taglist:
                    if tag not in taglist:
                        tag.delete()
                for tagname in taglist:
                    try:
                        tag = Tag.objects.get(name=tagname)
                    except Tag.DoesNotExist:
                        tag = Tag(name=tagname, user=request.user, organization=request.user.organization)
                        tag.save()
                    entry = TagEntry(tag=tag, message_id=question.message_id, user=question.user)
                    entry.save()
            return Response(question.serialize(), 201)

        return Response({"messages":messages},400)

    def get(self, request, question_id=None):
        '''
        Retrieves questions according to request parameters (such as question id, author id and tags)
        Functionality can be determined by providing different search parameters and searchInclusion method

        @params
            request: the request parameter from get function
            question_id, integer (optional): The id of the question to be retrieved
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
        @return
            200:
                list of retrieved questions
                example: {
                            "questions":[{
                                        "title":"What is the question?",
                                        "content":"An example question",
                                        "version":1,
                                        "user": {
                                            "username": "admin",
                                            "reputation": 0,
                                            "lastLogin": "2014-02-08T14:16:58.926Z",
                                            "firstName": "Ville",
                                            "created": "2014-01-05T19:53:55Z",
                                            "lastName": "Tolonen",
                                            "userId": 1,
                                            "email": "admin@admin.fi"
                                        },
                                        "created": "2014-01-08T11:05:16",
                                        "modified": "2014-01-08T11:05:16",
                                        "messageId": 4,
                                        }]
                        }
            404: No content found
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }
            400: Bad request, parameters were missing or wrong type
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
                        }
            401: Unauthorized, the user has to be logged in to perform this action
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
            403: Forbidden, the user does not have permission for the action
                list of appropriate error messages
                example: {
                            "messages":[{"content":"An example error message.","identifier":"example"}]
        '''

        if not request.user.is_authenticated():
            return Response(create_message("User must be logged in."), 401)

        messages = []
        question_sets = [] # list of question lists retrieved by different methods
        get_all = True # Flag for default return if no search parameters were provided

        if question_id:
            try:
                question = Question.objects.get(message_id=int(question_id), organization=request.user.organization)
                return Response(question.serialize_single(), 200)
            except ValueError:
                return Response({"messages": create_message("Given question id was invalid")}, 400)
            except Question.DoesNotExist:
                return Response(create_message("No question found"), 404)

        if request.GET.get("authorId"):
            get_all = False
            try:
                author = User.objects.get(user_id=int(request.GET.get("authorId")))
                question_sets.append(list(Question.objects.filter(user=author, organization=request.user.organization)))
            except User.DoesNotExist:
                question_sets.append([])

        if request.GET.get("authorName"):
            get_all = False
            try:
                author = User.objects.get(username=request.GET.get("authorName"))
                question_sets.append(list(Question.objects.filter(user=author, organization=request.user.organization)))
            except User.DoesNotExist:
                question_sets.append([])

        if request.GET.get("tags"):
            get_all = False
            tags = request.GET.get("tags").split(",")
            tags = unique(tags)

            tag_question_sets = [[] for tag in tags]    # Lists of questions corresponding each tag in the same order
            for ind, tag in enumerate(tags):
                # Get all tag entries for the tag
                try:
                    tag_entries = Tag.objects.get(name=tag).tagentry_set.all()
                except:
                    tag_entries = []
                # Fetch all questions corresponding the tag entries
                for tag_entry in tag_entries:
                    for question in Question.objects.filter(message_id=tag_entry.message_id):
                        tag_question_sets[ind].append(question)

            if request.GET.get("tagInclusion") in [None, "or"]:
                question_sets.append(unique([q for subset in tag_question_sets for q in subset]))
            else:
                question_sets.append(intersect(tag_question_sets))

        if get_all:
            question_sets.append(list(Question.objects.filter(organization=request.user.organization)))

        if request.GET.get("searchInclusion") in [None, "or"]:
            questions = unique([q for subset in question_sets for q in subset])
        else:
            questions = intersect(question_sets)

        if not questions or len(questions) == 0:
            return Response(create_message("No questions found"), 404)

        questions = exclude_old_versions(questions) # This should be modified, when we also want to retrieve question history

        try:
            questions = order_messages(questions, request.GET.get("order"))
        except ValueError:
            questions = order_messages(questions, "latest")

        try:
            questions = questions[:abs(int(request.GET.get("limit")))]
        except (ValueError, TypeError):
            questions = questions[:10]

        return Response({"questions": [question.serialize() for question in questions]}, 200)
