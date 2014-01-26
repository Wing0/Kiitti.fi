from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import *
from QnA.view_utils import *
import json

class UserAPI(APIView):

    def get(self, request):
        '''
        Get user objects.
        '''
        order = request.GET.get("order")
        if order is None or order == "all":
            return self.get_all()
        elif order == "organization":
            return self.get_by_organization_id(request.GET.get("organizationId"))
        elif order == "userid":
            return self.get_by_id(request.GET.get("userId"))
        else:
            return Response({"messages": "Invalid sorting type.", "identifier": ""}, 400)

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
            204: No content found. List of appropriate error messages.
                example:
                {
                    "messages":[{"content":"An exampleerror message.","identifier":"example"}]
                }
            400: Invalid parameters. List of appropriate error messages.
                example:
                {
                    "messages":[{"content":"An example error message.","identifier":"example"}]
                }
        '''
        if userid is None:
            return Response({"messages": "User id does not exist.", "identifier": "userid"}, 400)
        try:
            userid = int(userid)
            if userid < 0:
                raise ValueError()
            return Response({"users": User.objects.get(user_id=usersid).serialize()}, 200)
        except ValueError:
            return Response({"messages":[{"content":"User id is not positive integer.","identifier":"userid"}]}, 400)
        except:
            return Response({"messages":[{"content":"No user with given id.","identifier":"userid"}]}, 204)

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
                        "firstname":"Aalto",
                        "lastname": "Aaltonen",
                        "username": "Wingo",
                        "created":"01.01.2014 16:33:41",
                        "email":"aalto@aalto.fi",
                        "password": "hashedpassword",
                        .....
                        }
                    ]
                }
            204: No content found. List of appropriate error messages.
                example:
                {
                    "messages":[{"content":"An exampleerror message.","identifier":"example"}]
                }
            400: Invalid parameters. List of appropriate error messages.
                example:
                {
                    "messages":[{"content":"An example error message.","identifier":"example"}]
                }

        '''
        if orgid is None:
            return Response({"messages": "Organization id does not exist.", "identifier": "orgid"}, 400)
        try:
            orgid = int(orgid)
            if orgid < 0:
                raise ValueError()
            data = []
            users = User.objects.filter(organization=orgid)
            for user in users:
                data.append(user.serialize())
            return Response({"users": data}, 200)
        except ValueError:
            return Response({"messages":[{"content":"Organization id is not positive integer.","identifier":"orgid"}]}, 400)
        except:
            return Response({"messages":[{"content":"No user with given id.","identifier":"orgid"}]}, 204)

    def get_all(self):
        '''
        Get all users.
        '''
        data = []
        userdata = User.objects.all()
        for user in userdata:
            data.append(user.serialize())
        return Response({"users": data}, 200)
