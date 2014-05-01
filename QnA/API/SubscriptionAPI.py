# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions as exc

from QnA.exceptions import NotFound
from QnA.models import Subscription
from QnA.serializers import SubscriptionSerializerGET, SubscriptionSerializerPOST
from QnA.utils import create_message

class SubscriptionAPI(APIView):


    def get(self, request):
        if request.user.is_staff:
            return self.get_many(request)
        return Response(create_message("User does not have permisson to get subscriptions."), 401)

    def get_many(self, request):
        subs = Subscription.objects.all()
        if not subs:
            raise NotFound("No subscriptions found.")
        serializer = SubscriptionSerializerGET(subs, many=True)
        return Response(serializer.data, 200)


    def post(self, request):
        email = request.DATA.get("email", None)
        if email is None:
            raise exc.ParseError("No email for subscription provided.")
        if self.is_subscribed(email):
            return Response(create_message("Email is already subscribed."), 400)
        serializer = SubscriptionSerializerPOST(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(create_message("New subscription created."), 201)
        raise exc.ParseError("Subscription could not be created.")


    def is_subscribed(self, email):
        try:
            sub = Subscription.objects.get(email=email)
            return True
        except Subscription.DoesNotExist:
            return False
