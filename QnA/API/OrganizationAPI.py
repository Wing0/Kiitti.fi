# -*- coding: utf-8 -*-

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import rest_framework.exceptions as exc

from QnA.models import Organization
from QnA.serializers import OrganizationSerializerGET, OrganizationSerializerPOST
from QnA.exceptions import NotFound
from QnA.view_utils import *
from QnA.utils import *


class OrganizationAPI(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, organization_id=None):
        if organization_id:
            return self.get_single(request, organization_id)

        return self.get_many(request)

    def get_many(self, request):

        organizations = Organization.objects.all()
        if not organizations:
            raise NotFound("No organizations could be found.")

        serializer = OrganizationSerializerGET(organizations, many=True)

        return Response(serializer.data, 200)


    def get_single(self, request, organization_id):
        # todo: check that user has permissions to get organization
        # todo: messages

        try:
            organization = Organization.objects.get(organization_id=organization_id)
        except Organization.DoesNotExist:
            raise NotFound("Requested organization cannot be found.")

        serializer = OrganizationSerializerGET(organization)

        return Response(serializer.data, 200)


    def post(self, request):

        if not request.DATA.get("name", None):
            raise exc.ParseError("Organization name must be provided.")
        if not request.DATA.get("address", None):
            raise exc.ParseError("Organization address must be provided.")

        serializer = OrganizationSerializerPOST(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(create_message("New organization created."), 201)
        else:
            return Response(serializer.errors, 400)

        raise ParseError("Organization could not be created")

