from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import *
from QnA.utils import *
import json


class TagAPI(APIView):

    def post(self, request):
        '''
        @params
            courseFlag: Determines whether tag is related to course or not.
            name: Name of tag.
        @example
            {
                "courseFlag": "false",
                "name": "Mathematics"
            }
        @returns
            201: If Tag was created successfully.
            400: If user input is invalid.
            401: If user is not logged in.
        '''
        messages = []
        course_flag = request.GET.get("courseFlag")
        name = request.GET.get("name")
        if not request.user.is_authenticated():
            return Response(create_message("You must be logged in to request comments."), 401)
        if string_to_boolean(course_flag) == None:
            messages.append(compose_message("Course flag must be a boolean value.", "courseFlag"))
        if name == None or len(name) == 0:
            messages.append(compose_message("Name must be non-empty string.", "name"))
        if len(messages) == 0:
            tag = Tag(organization=request.user.organization, course_flag=course_flag, name=name)
            tag.user = request.user
            messages = tag.validate()
            if len(messages) == 0:
                tag.save()
                return Response(create_message("New tag was created successfully."), 201)

        return Response({"messages": messages}, 400)


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
