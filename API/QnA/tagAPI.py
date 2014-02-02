from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import *
from QnA.utils import *
import json

def create_tag(organization_id, name, course_flag, creator):
    messages = []
    success= False
    return success, messages


def validate_input(request):
    # Get the data from the request
    data = json.loads(request.body)

    # Validate organizationId and find the Organization object
    organization_id = data.get("organizationId")
    if organization_id == None:
        valid = False
        messages.append({"type": "alert", "content": "Organization id is missing.", "identifier": "organizationId"})
    else:
        if isinstance(organization_id, int):
            try:
                organization = Organization.objects.get(organization_id = organization_id)
            except:
                messages.append({"type": "alert", "content": "Organization id did not match any organization.", "identifier": "organizationId"})
        else:
            messages.append({"type": "alert", "content": "Organization id must be a positive integer.", "identifier": "organizationId"})

    # Validate tag name
    name = data.get("name")
    if not name:
        valid = False
        messages.append({"type": "alert", "content": "Tag name is missing.", "identifier": "name"})
    elif not isinstance(name, basestring):
        valid = False
        messages.append({"type": "alert", "content": "Tag name must be a string.", "identifier": "name"})

    # Validate course flag
    course_flag =  data.get("courseFlag")
    if course_flag == None:
        valid = False
        messages.append({"type": "alert", "content": "Coursee flag information is missing.", "identifier": "courseFlag"})
    elif not course_flag in [True, False]:
        valid = False
        messages.append({"type": "alert", "content": "Coursee flag must be a boolean value.", "identifier": "courseFlag"})

    # Validate user id and find the corresponding User object
    user = None
    user_id = data.get("userId")
    if user_id == None:
        # Default action: use the logged in user if user id is not provided
        if request.user.is_authenticated():
            user = request.user
        else:
            valid = False
            messages.append({"type": "alert", "content": "Please log in or provide user id.", "identifier": "userId"})
    else:
        if isinstance(user_id, int):
            try:
                # ToDo: Check user rights for using this user id
                user = User.objects.get(user_id=user_id)
            except:
                valid = False
                messages.append({"type": "alert", "content": "Provided user id does not match any user.", "identifier": "userId"})
        else:
            valid = False
            messages.append({"type": "alert", "content": "User id has to be a positive integer.", "identifier": "userId"})

    return valid, messages, [organization, name, course_flag, user]

class TagAPI(APIView):

    def post(self, request):
        success = False

        # Input validation
        valid_input, messagesm, [organization, name, course_flag, user] = validate_input(request)

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
