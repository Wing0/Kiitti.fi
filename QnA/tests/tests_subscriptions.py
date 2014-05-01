# -*- coding: utf-8 -*-
from QnA.models import Subscription
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory

from QnA.API.SubscriptionAPI import SubscriptionAPI


class SubscriptionTests(APITestCase):

    def setUp(self):

        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.url = "/subscriptions"

    def test_valid_email(self):
        request = self.client.post(self.url, {"email": "test@test.test"})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED,
                         "Response status code was %s (expected 201)" % request.status_code)

    def test_invalid_email(self):

        invalid_emails = ["ema@asdf.", "asdf.asdf.sadf", "asfd@asdf@asdf.fadsf",
                          "asdf.@.asdf.asdf", "asdf@asdf"]

        for email in invalid_emails:
            request = self.client.post(
                "/subscriptions", {"email": email})
            self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST,
                             "Response status code was %s (expected 400)" % request.status_code)

    def test_duplicate_email(self):
        self.client.post(self.url, {"email": "test@test.test"})
        request = self.client.post(self.url, {"email": "test@test.test"})
        self.assertEqual(request.status_code, status_code.HTTP_200_OK,
                         "Response status code was %s (expected 200)" % request.status_code)
