# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions as exc

from QnA.exceptions import NotFound

from django.conf import settings

import mailchimp


class SubscriptionAPI(APIView):

    def post(self, request):
        m = mailchimp.Mailchimp(settings.MAILCHIMP_APIKEY)
        list_id = settings.MAILCHIMP_LISTID

        email = request.DATA.get('email', None)
        if not email:
            raise exc.ParseError("Email is empty", 400)

        try:
            m.lists.subscribe(list_id, {'email': email})
            return Response("The email has been successfully subscribed", 200)
        except mailchimp.ListAlreadySubscribedError:
            return Response("That email is already subscribed to the list", 214)
        except mailchimp.Error, e:
            return Response("An error occurred: %s - %s" % (e.__class__, e), 400)
