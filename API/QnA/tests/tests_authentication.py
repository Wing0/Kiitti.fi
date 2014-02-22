from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status

from QnA.API import LoginAPI
from QnA.models import User, Organization


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.organization = Organization(organization_id=1, name="testorganization")
        self.user = User.objects.create_user(
            username='test', email='test@test.test', password='test', organization=self.organization)

    def test_login(self):
        request = self.factory.get('/auth/login', {"username": "test", "password": "test"})

        view = LoginAPI.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
