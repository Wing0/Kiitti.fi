from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import *
from QnA.view_utils import *
from QnA.utils import *
import json

class UserAPI(APIView):

    def get(self, request):
        '''
        Get user objects.
        '''
        if not request.user.is_authenticated():
            return Response(create_message("You must be logged in to request userdata."), 403)
        order = request.GET.get("order")
        if order is None or order == "all":
            return self.get_all()
        elif order == "organization":
            try:
                orgid = request.GET.get("organizationId")
                if orgid is None:
                    raise ValueError()
                orgid = int(orgid)
                return self.get_by_organization_id(orgid)
            except ValueError:
                return Response(create_message("Organization id is not positive integer.", "orgid"), 400)
        elif order == "userid":
            try:
                userid = request.GET.get("userId")
                if userid is None:
                    raise ValueError()
                userid = int(userid)
                return self.get_by_id(userid)
            except ValueError:
                return Response(create_message("User id is not positive integer.", "userId"), 400)
        else:
            return Response(create_message("Invalid sorting type.", "order"), 400)

    #VALIDATE
    def post(self, request):
        '''
        @example:
            {
              "username":"test",
              "password":"test",
              "organizationId":1,
              "email":"test@test.test",
              "firstName":"test",
              "lastName":"test"
            }
        '''
        data = json.loads(request.body)
        messages = []
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

            messages = user.validate()
            if len(messages) == 0:
                user.set_password(user.password)
                try :
                    user.save()
                    return Response({"messages": "New user created."}, 201)
                except IntegrityError, e:
                    valid = False
                    if e.message == "column username is not unique":
                        messages.append(compose_message("Username already in use."))
                    else:
                        messages.append(compose_message(e.message))
        else:
            messages.append(compose_message("Something is missing"))
        return Response({"messages": messages}, 400)


    def get_by_id(self, userid):
        '''
        Get User by id.

        @params
            userid, int: User id which should be returned.
        @example
            /user/?userId=223
        @perm
            member: Get basic information aabout Organization.
            staff: Shows additional information about Organization.
            admin: Load all Organizations.
        @return
            200: Found User.
                example:
                {
                    "users":[
                        {
                            "username": "admin",
                            "firstname": "Admin",
                            "lastname": "Adminen",
                            "email": "admin@admin.org",
                            "reputation": 0,
                            "userId": 1,
                            "created": "2014-01-25T18:28:28.520Z"
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
        if not isinstance(userid, int) or userid < 0:
           messages.append(compose_message("User id must be positive integer.", "userid"))
        if len(messages) == 0:
            try:
                return Response({"users": User.objects.get(user_id=usersid).serialize()}, 200)
            except:
                messages.append(compose_message("No user with given id.", "userid"))
        return Response({"messages": messages}, 400)


    def get_by_organization_id(self, orgid):
        '''
        Get users related to given organization.

        @param
            orgid, string: Organization id in string format.
        @example
            /users/?organizationId=123
        @return
            200: Found Users.
                example:
                {
                    "users":[
                        {
                            "username": "admin",
                            "firstname": "Admin",
                            "lastname": "Adminen",
                            "email": "admin@admin.org",
                            "reputation": 0,
                            "userId": 1,
                            "created": "2014-01-25T18:28:28.520Z"
                        },
                        {
                            "username": "test",
                            "firstname": "test",
                            "lastname": "Testaaja",
                            "email": "testn@admin.org",
                            "reputation": 0,
                            "userId": 2,
                            "created": "2014-01-26T18:28:28.520Z"
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
        if not isinstance(orgid, int) or orgid < 0:
            messages.append(compose_message("Organization id must be positive integer.", "orgid"))
        if len(messages) == 0:
            try:
                data = []
                users = User.objects.filter(organization=orgid)
                for user in users:
                    data.append(user.serialize())
                return Response({"users": data}, 200)
            except:
                messages.append(compose_message("No organization found.", "organization_id"))
        return Response({"messages": messages}, 400)

    def get_all(self):
        '''
        Get all users.
        '''
        data = []
        userdata = User.objects.all()
        for user in userdata:
            data.append(user.serialize())
        return Response({"users": data}, 200)
