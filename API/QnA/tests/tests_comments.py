from QnA.models import User, Organization, Comment
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from django.core.management import call_command

from QnA.API.CommentAPI import CommentAPI
from QnA.API.LoginAPI import LoginAPI

class CommentTests(APITestCase):

    def setUp(self):
        call_command('loaddata', 'initial_data')
        self.factory = APIRequestFactory()


    def post_test_message(self, url, data, view):
        request = self.factory.post(url, data, format="json")
        request.user = User.objects.get(username="admin")
        response = view(request)
        error = "201 should have been returned. %s returned instead." % str(response.status_code)
        self.assertEquals(response.status_code, 201, error)
        self.comment_equals(data, response.data)

    def comment_equals(self, first_data, second_data):
        self.assertEquals(first_data.get("content"), second_data.get("content"), "Contents of comment are not equal.")
        self.assertEquals(first_data.get("parentId"), second_data.get("parentId"), "Parent id of comments are not equal.")
        self.assertEquals(first_data.get("isQuestion"), second_data.get("isQuestion"), "IsQuestion value is not equal.")


    def test_unauthorized_access(self):
        data = {
            "content": "This is content created in CommentTests.",
            "parentId": 1,
            "isQuestion": True
        }
        self.unauthorized_access("/comments/", data, CommentAPI.as_view())

    def unauthorized_access(self, url, data, view):
        #get-test
        request = self.factory.get(url)
        response = view(request)
        error = "401 should have been returned. %s returned instead." % str(response.status_code)
        self.assertEquals(response.status_code, 401, error)
        #post-test
        request = self.factory.post(url, data, format="json")
        response = view(request)
        error = "401 should have been returned. %s returned instead." % str(response.status_code)
        self.assertEquals(response.status_code, 401, error)


    def test_authorized_access(self):
        data = {
            "content": "This is content created in CommentTests.",
            "parentId": 1,
            "isQuestion": True
        }
        self.authorized_access("/comments/", data, CommentAPI.as_view())

    def authorized_access(self, url, data, view):
        #get-test
        request = self.factory.get(url)
        request.user = User.objects.get(username="admin")
        response = view(request)
        error = "200 should have been returned. %s returned instead." % str(response.status_code)
        self.assertEquals(response.status_code, 200, error)
        #post-test
        self.post_test_message(url, data, view)



    def test_new_version(self):
        data = {
            "content": "This is something new...",
            "parentId": 1,
            "isQuestion": True
        }
        self.new_version("/comment/", data, "I am the new content!!!", CommentAPI.as_view())


    def new_version(self, url, data, content, view):
        request = self.factory.post(url, data, format="json")
        request.user = User.objects.get(username="admin")
        response_first = view(request)
        self.assertEquals(response_first.status_code, 201, "%s was returned instead of 201" % str(response_first.status_code))
        self.comment_equals(data, response_first.data)

        data["messageId"] = response_first.data.get("messageId")
        data["content"] = content
        request = self.factory.post(url, data, format="json")
        request.user = User.objects.get(username="admin")
        response = view(request)
        self.assertEquals(response.status_code, 201, "%s was returned instead of 201" % str(response.status_code))
        self.comment_equals(data, response.data)
        self.assertEquals(data.get("messageId"), response.data.get("messageId"), "Message id is not equal.")
        self.assertNotEquals(response_first.data.get("content"), response.data.get("content"), "Contents should be different.")


    def test_get_by_parent(self):
        #add one comment
        data = {
            "content": "The test!!!",
            "parentId": 1,
            "isQuestion": True
        }
        self.post_test_message("/comments/",data, CommentAPI.as_view())

        data = {
            "parentId": 1,
            "isQuestion": True
        }
        request = self.factory.get("/comments/", data)
        request.user = User.objects.get(username="admin")
        view = CommentAPI.as_view()
        response = view(request)
        error = "200 should have been returned. %s returned instead." % str(response.status_code)
        self.assertEquals(response.status_code, 200, error)
        exist = False
        for item in response.data.get("comments"):
            if item.get("content") == "The test!!!":
                exist = True
                break
        self.assertEquals(exist, True, "Search by parent does not return correct messages.")
