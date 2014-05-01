# -*- coding: utf-8 -*-
from QnA.models import User
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from django.core.management import call_command


class BaseTest(APITestCase):

    def setUp(self):
        call_command('loaddata', 'min_test_data')
        self.factory = APIRequestFactory()


    def post_message(self, url, data, view, user="admin", **kwargs):
        '''
        Posts data to server.

        @params
            url, string: Url where data should be sent.
            data, dictionary: Post parameters to be sent.
            view, APIView: View which should handle this post request.
            user, string: Name of user who made this request.
        @returns
            response-object.
        '''
        request = self.factory.post(url, data, format="json")
        request.user = User.objects.get(username=user)
        return view(request, **kwargs)

    def get_message(self, url, data, view, user="admin"):
        '''
        Gets data from server.

        @params
            url, string: Url where data should be retrieved.
            data, dictionary: Get parameters to be sent.
            view, APIView: View which should handle this get request.
            user, string: Name of user who made this request.
        @returns
            response-object.
        '''
        request = self.factory.get(url, data, format="json")
        request.user = User.objects.get(username=user)
        return view(request)

    def create_message(self, url, data, view, **kwargs):
        '''
        Checks was this message successfully created.
        '''
        response = self.post_message(url, data, view, "admin", **kwargs)
        error = "201 should have been returned. %i returned instead." % response.status_code

        #check whether message was created and then return response
        self.assertEquals(response.status_code, 201, error)
        return response


    def unauthorized_access(self, url, data, view):
        '''
        Test for unauthorized access.

        '''
        #get-test
        request = self.factory.get(url)
        response = view(request)
        error = "401 should have been returned. %i returned instead." % response.status_code
        self.assertEquals(response.status_code, 401, error)

        #post-test
        request = self.factory.post(url, data, format="json")
        response = view(request)
        error = "401 should have been returned. %i returned instead." % response.status_code
        self.assertEquals(response.status_code, 401, error)
        return response
