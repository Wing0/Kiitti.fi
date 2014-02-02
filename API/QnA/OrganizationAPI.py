from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import Organization
from QnA.view_utils import *
from QnA.utils import *
import json


class OrganizationAPI(APIView):

    def get(self, request):
        '''
        Get Organization. Heigher permissions returns more content to user.
        '''
        if not request.user.is_authenticated():
            return Response(create_message("You must be logged in to request comments."), 403)
        order = request.GET.get("order")
        if order is None or order == "all":
            return self.get_all()
        elif order == "id":
            return self.get_by_id(request.GET.get("organizationId"))


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
        if not data.get("organization_id"):
            messages.append({"type": "alert","content": "Organization id must be provided.","identifier": "organizationId"})
        if valid_input:
            org = Organization(name=data.get("name"), address=data.get("address"), organization_id=data.get("organizationId"))
            valid, messages = org.validate()
            if valid:
                org.save()
                success = True
        return Response({"messages":messages, "success":success}, 200)

    def get_by_id(self, orgid):
        '''
        Get Organization by id.

        @params
            orgid, string: Organization id which should be returned.
        @example
            /organization/?organizationId=223
        @perm
            member: Get basic information aabout Organization.
            staff: Shows additional information about Organization.
            admin: Load all Organizations.
        @return
            200: Found organization.
                example:
                {
                    "organizations":[
                        {
                        "name":"Aalto",
                        "organizationId":"1",
                        "created":"2014-01-25T18:28:28.520Z",
                        "modified":"2014-01-25T18:28:28.520Z",
                        "address":"Aallonkuja 4 A 13"
                        }
                    ]
                }
            400: Bad request. List of appropriate error messages.
                example:
                {
                    "messages":[{"content":"An exampleerror message.","identifier":"example"}]
                }
        '''
        messages = []
        try:
            if not isinstance(orgid, int) or orgid < 0:
                messages.append(compose_message("Organization id must be positive integer.", "orgid"))
            if len(messages) == 0:
                return Response({"organizations": Organization.objects.get(organization_id=orgid).serialize()}, 200)
        except:
            messages.append(compose_message("No Organization with given id exist.", "orgid"))
        return Response({"messages": messages}, 400)

    def get_all(self):
        data = []
        orgdata = Organization.objects.all();
        for org in orgdata:
            data.append(org.serialize())
        return Response({"organizations": data}, 200)
