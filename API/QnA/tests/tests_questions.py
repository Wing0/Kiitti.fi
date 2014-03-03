# -*- coding: utf-8 -*-
from QnA.models import User, Organization, Question
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory

from django.core.management import call_command

from QnA.API.QuestionAPI import QuestionAPI
from QnA.API.LoginAPI import LoginAPI


def flush_questions():
    # Ensure empty questions:
    Question.objects.all().delete()


class QuestionTests(APITestCase):

    def setUp(self):
        call_command('loaddata', 'min_test_data')
        self.client = APIClient()
        self.factory = APIRequestFactory()

        self.organization = Organization(
            rid=1, name="testorganization")
        self.user = User(
            username='test', email='test@test.test', password='test', organization=self.organization)

    def validate_question(self, retrieved_question, given_data, user=False):
        # Test tags
        retrieved_tags = retrieved_question.get("tags")
        given_tags = given_data.get("tags")

        for tag in given_tags:
            self.assertIn(
                tag, retrieved_tags, "%s was not in the tags of the created question" % tag)

        for tag in retrieved_tags:
            self.assertIn(
                tag, given_tags, "%s was not supposed to be in the tags of the created question" % tag)

        # Test content
        self.assertEqual(given_data["title"], retrieved_question[
                         "title"], "Title was not same as in given data")
        self.assertEqual(given_data["content"], retrieved_question[
                         "content"], "Content was not same as in given data")

        # Test user data
        if user:
            self.assertEqual(
                user.username, retrieved_question["user"]["username"],
                "The username (%s) was different to that of the creator (%s)" % (
                    user.username, retrieved_question["user"]["username"]
                )
            )

    def test_post_get_question(self):
        self.client.login(username='test', password='test')

        # keys that will be checked
        question_keys = ['messageId', 'content', 'title', 'created', 'tags'] # todo: add more

        # post question and check return data
        request = self.client.post(
            "/questions", {"title": "testtitle", "content": "testcontent", "tags": "tag1 tag2"})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED,
                         "Response status code was %s (should be 201)" % request.status_code)

        for key in question_keys:
            self.assertIsNotNone(request.data.get(key, None),
                "Response does not contain key '%s'" % key)

        # get question and check data
        request = self.client.get(
            "/questions/%d" % request.data.get('messageId'))
        for key in question_keys:
            self.assertIsNotNone(request.data.get(key, None),
                "Response does not contain key '%s'" % key)

    def test_unauthorized_access(self):
        url = "/questions/"
        data = {}
        # get
        request = self.factory.get(url)
        view = QuestionAPI.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         "Response status code %s was not 401" % response.status_code)
        # post
        data = {
            "title": "Why does the sun go down every night?",
            "content": "Why does the sun go down every night? I don't understand!",
            "tags": ["tagFirst", "tagSecond"]
        }
        request = self.factory.post(url, data)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
                         "Response status code %s was not 401" % response.status_code)

    def test_authorized_access(self):
        flush_questions()

        # get empty
        url = "/questions/"
        request = self.factory.get(url)
        request.user = User.objects.get(username="admin")
        view = QuestionAPI.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                         "Response status code %s was not 404" % response.status_code)

        data = {
            "title": "Why does the sun go down every night?",
            "content": "Why does the sun go down every night? I don't understand!",
            "tags": ["tagFirst", "tagSecond"]
        }
        request = self.factory.post(url, data)
        request.user = User.objects.get(username="admin")
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         "Response status code %s was not 201" % response.status_code)

        # test question attributes
        self.validate_question(response.data, data, request.user)

        # test populated get
        url = "/questions/"
        request = self.factory.get(url)
        request.user = User.objects.get(username="admin")
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         "Response status code %s was not 200" % response.status_code)

    def test_duplicates(self):
        flush_questions()

        url = "/questions/"
        data = {
            "title": "Why does the sun go down every night?",
            "content": "Why does the sun go down every night? I don't understand!",
            "tags": ["tagFirst", "tagSecond"]
        }
        request = self.factory.post(url, data)
        request.user = User.objects.get(username="admin")
        view = QuestionAPI.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         "Response status code %s was not 201" % response.status_code)

        request = self.factory.post(url, data)
        request.user = User.objects.get(username="admin")
        response = view(request)
        # Creating same question twice
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
                         "Response status code %s was not 400" % response.status_code)

    def test_edit(self):
        flush_questions()

        # Create initial question
        url = "/questions/"
        data = {
            "title": "Why does the sun go down every night?",
            "content": "Why does the sun go down every night? I don't understand!",
            "tags": ["tagFirst", "tagSecond"]
        }
        request = self.factory.post(url, data)
        request.user = User.objects.get(username="admin")
        view = QuestionAPI.as_view()
        response = view(request)
        msg_id = response.data.get("messageId")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         "Response status code %s was not 201" % response.status_code)
        self.validate_question(response.data, data, request.user)

        # Edit question
        data_edited = {
            "title": "Why does the sun go down?",
            "content": "Why does the sun go down every night? I don't understand!",
            "messageId": msg_id,
            "tags": ["tagSecond", "tagThird"]
        }
        request = self.factory.post(url, data_edited)
        request.user = User.objects.get(username="admin")
        response = view(request)
        # Edit existing question
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.validate_question(response.data, data_edited, request.user)

        # Test edited question attributes
        tags = response.data.get("tags")
        self.assertNotIn("tagFirst", tags, "tagFirst was in created question")

    def test_scandinavian(self):
        flush_questions()

        # Try scandinavian
        url = "/questions/"
        data = {
            "title": u"Tämä on suomenkielinen kysymys, vai onko?",
            "content": u"Miksi ä, ö ja å -kirjamet eivät toimi",
            "tags": ["tagFirst", "tagSecond"]
        }
        request = self.factory.post(url, data)
        request.user = User.objects.get(username="admin")
        view = QuestionAPI.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         "Response status code %s was not 201" % response.status_code)
        self.validate_question(response.data, data, request.user)
