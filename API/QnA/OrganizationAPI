from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.views import APIView
from QnA.models import *
import json

class OrganizationAPI(APIView):

    def get(self, request):
        '''
        Get answers
        @params
            id: Organization id to
        @return:
            200:

        '''
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
