from QnA.models import User, Organization
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from django.core.management import call_command

from QnA.QuestionAPI import QuestionAPI
from QnA.LoginAPI import LoginAPI

class QuestionTests(APITestCase):

    def setUp(self):
        call_command('loaddata', 'min_test_data')
        self.factory = APIRequestFactory()

    def test_unauthorized_access(self):
        url = "/questions/"
        data = {}
        request = self.factory.get(url, data, format='json')
        view = QuestionAPI.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_access(self):
        url = "/auth/login/"
        data = {}
        request = self.factory.post(url, data, format='json')
        view = LoginAPI.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creation(self):
        pass
