from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import *
from QnA.view_utils import *
import json

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
