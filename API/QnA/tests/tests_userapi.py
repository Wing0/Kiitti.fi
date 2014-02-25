# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from QnA.models import User, Organization
from QnA.API.UserAPI import UserAPI


class UserAPITests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.organization = Organization(
            organization_id=1, name="testorganization")
        self.organization.save()
        self.user = User.objects.create_user(
            username='test', email='test@test.test', password='test', organization=self.organization)

    def test_post_user(self):
        """ Simple POST test """

        self.client.login(username='test', password='test')

        # try posting valid user
        request = self.client.post(
            '/users', {
                "username": "newtestuser",
                "email": "test@email.test",
                "password": "testpassword",
                "organization": 1
            })

        self.assertEqual(request.status_code, status.HTTP_201_CREATED,
            "\nCould not post a valid user.\n"
            "Response: %s\n"
            "Response status code was %s (should be 201)"
            % (request.status_code, request.content))

        # check that user was really created
        try:
            user = User.objects.get(username='newtestuser')
        except User.DoesNotExist:
            raise AssertionError("Could not find user as created")
