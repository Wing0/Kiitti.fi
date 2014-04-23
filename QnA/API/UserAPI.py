# -*- coding: utf-8 -*-

from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.exceptions as exc

from QnA.models import User
from QnA.serializers import UserSerializerGET, UserSerializerPOST
from QnA.exceptions import NotFound
from QnA.utils import compose_message, create_message


class UserAPI(APIView):

    def get(self, request, user_id=None):

        if user_id:
            return self.get_single(request, user_id)

        return self.get_many(request)

    def get_single(self, request, user_id):

        try:
            user = User.objects.get(rid=user_id)
        except User.DoesNotExist:
            raise NotFound("User could not be found.")

        serializer = UserSerializerGET(user)

        return Response(serializer.data, 200)

    def get_many(self, request):

        users = User.objects.all()

        if request.GET.get("user_id", None):
            users = users.filter(rid=request.GET['user_id'])
        if request.GET.get("organization_id", None):
            users = users.filter(organization=request.GET['organization_id'])

        if not users:
            raise NotFound("No users could be found.")

        serializer = UserSerializerGET(users, many=True)

        return Response(serializer.data, 200)

    def post(self, request):
        """ Creates new user
            @example request: {
              "username": "exampleusername",
              "password": "examplepassword",
              "organization_id": 1,
              "email": "ex@mple.email",
              "first_name": "examplefirstname",
              "last_name": "examplelastname"}
        """

        serializer = UserSerializerPOST(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
        else:
            return Response(serializer.errors, 400)

        raise ParseError("User could not be created")

    def put(self, request, user_id):
        """ Updates user
        """
        # todo: add user updating
        pass
