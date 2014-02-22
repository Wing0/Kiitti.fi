from django.test import TestCase, Client
from QnA.models import User

# Create your tests here.

class CommentTest(TestCase):


    def testGet(self):
        c = Client()
        reponse = c.get("/users?id=1")
        user = User.objects.get(user_id=1)
        self.assertEqual(reponse.user, user)

    def testSec(self):
        self.assertEqual(1, 0)
