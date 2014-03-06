# -*- coding: utf-8 -*-
from QnA.models import User
from QnA.tests.basetest import BaseTest
from QnA.API.CommentAPI import CommentAPI
from QnA.API.AnswerAPI import AnswerAPI
from QnA.API.QuestionAPI import QuestionAPI

class CommentTest(BaseTest):


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

    def create_answer(self):
        q = self.create_question()
        data = {
            "content": "Why does the sun go down every night? I don't understand!"
        }
        response_answer = self.create_message("/answers/", data, AnswerAPI.as_view(), rid=q.get("rid"))
        self.assertNotEquals(response_answer.data.get("rid"), None, "MessageRID is not determined.")
        return response_answer.data

    def test_unauthorized_access(self):
        data = {
            "content": "This is content created in CommentTests."
        }
        self.unauthorized_access("/comments/", data, CommentAPI.as_view())


    def test_post_question_comment(self):
        q = self.create_question()
        data = {
            "content": "This is content created in CommentTests."
        }
        self.create_message("/comment/", data, CommentAPI.as_view(), content_type="question", rid=q.get("rid"))

    def test_post_answer_comment(self):
        a = self.create_answer()
        data = {
            "content": "This is content created in CommentTests."
        }
        self.create_message("/comment/", data, CommentAPI.as_view(), content_type="answer", rid=a.get("rid"))
