from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from rest_framework import status

from QnA.API.LoginAPI import LoginAPI
from QnA.models import User, Organization


class AuthenticationTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.organization = Organization(
            organization_id=1, name="testorganization")
        self.user = User.objects.create_user(
            username='test', email='test@test.test', password='test', organization=self.organization)

    def test_login(self):
        request = self.client.post(
            '/auth/login', {"username": "test", "password": "test"})
        token = request.data.get('token', None)
        self.assertIsNotNone(
            token, "Could not receive authentication token on login post.")
        self.assertEqual(request.status_code, 200,
                         "Status code on /auth/login was not 200.")

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        request = self.client.get('/auth/load')
        self.assertEqual(request.status_code, 200,
                         "Status code on /auth/load was not 200.")
        self.assertEqual(request.data['username'], self.user.username,
                         "Usernames for loaded user and initialized user do not match.")
