# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from QnA.models import Vote, User, Organization
from QnA.API.VoteAPI import VoteAPI


class VoteAPITests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.organization = Organization(
            organization_id=1, name="testorganization")
        self.user = User.objects.create_user(
            username='test', email='test@test.test', password='test', organization=self.organization)

    def test_post_vote(self):
        self.client.login(username='test', password='test')

        # try posting vote with invalid direction
        request = self.client.post(
            '/votes', {"message_id": 111, "direction": 2})
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST,
            "Posting invalid vote. "
            "Response status code was %s (should be 400)" % request.status_code)

        # try posting valid vote
        request = self.client.post(
            '/votes', {"message_id": 111, "direction": 1})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED,
            "Could not post a valid vote. "
            "Response status code was %s (should be 201)" % request.status_code)

        # check that vote was really created
        try:
            vote = Vote.objects.get(message_id=111, direction=1, user=self.user)
        except Vote.DoesNotExist:
            raise AssertionError("Could not find vote as created")

        # update vote with new direction
        request = self.client.post(
            '/votes', {"message_id": 111, "direction": -1})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED,
            "Existing vote with new direction failed. "
            "Response status code was %s (should be 201)" % request.status_code)

        # check that vote with old direction cannot be found
        try:
            vote = Vote.objects.get(message_id=111, direction=1, user=self.user)
            raise AssertionError("Vote was not properly updated")
        except Vote.DoesNotExist:
            pass

    def test_unauthorized_access(self):
        request = self.client.post(
            '/votes', {"message_id": 111, "direction": 1})
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED,
            "Response status code was %s (should be 401)" % request.status_code)
