# -*- coding: utf-8 -*-
from QnA.models import User
from QnA.tests.basetest import BaseTest
from QnA.API.AnswerAPI import AnswerAPI
from QnA.API.QuestionAPI import QuestionAPI


class AnswerTest(BaseTest):


    def create_question(self):
        data = {
            "head":{
                "title": "Why does the sun go down every night?"
            },
            "content": "Why does the sun go down every night? I don't understand!",
            "tags": ["tagFirst", "tagSecond"]
        }
        response = self.create_message("/questions/", data, QuestionAPI.as_view())
        return response.data


    def test_unauthorized_access(self):
        data = {
            "content": "This is content created in AnswerTests."
        }
        self.unauthorized_access("/answers/", data, AnswerAPI.as_view())


    def test_post(self):
        q = self.create_question()
        data = {
            "content": "This is content created in AnswerTests."
        }
        response = self.create_message("/answers/", data, AnswerAPI.as_view(), rid=q.get("rid"))
        error = "201 should have been returned. %i returned instead." % response.status_code
        self.assertEquals(response.status_code, 201, error)



