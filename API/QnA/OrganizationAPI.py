from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import Organization
from QnA.view_utils import *
import json

def get_by_id(orgid):
    '''
    Get Organization by id.

    @params
        orgid, int: Organization id which should be returned.
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
                    "created":"01.01.2014 16:33:41",
                    "modified":"15.01.2014 08:10:22",
                    "address":"Aallonkuja 4 A 13"
                    }
                ]
            }
        204: No content found. List of appropriate error messages.
            example:
            {
                "messages":[{"content":"An exampleerror message.","identifier":"example"}]
            }
    '''
    try:
        return Response({"organizations": Organization.objects.get(organization_id=orgid).serialize()}, 200)
    except:
        return Response({"messages":[{"content":"No organization with given id.","identifier":"orgid"}]}, 204)

class OrganizationAPI(APIView):

    def get(self, request):
        '''
        Get Organization. Heigher permissions returns more content to user.
        '''
        try:
            return get_by_id(int(request.GET.get("organizationId")))
        except ValueError:
            return Response({"messages":[{"content":"Organization id is not integer.","identifier":"organizationId"}]}, 400)

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
