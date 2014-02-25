from django.conf.urls import patterns, include, url
from QnA.API.AnswerAPI import AnswerAPI
from QnA.API.UserAPI import UserAPI
from QnA.API.CommentAPI import CommentAPI
from QnA.API.QuestionAPI import QuestionAPI
from QnA.API.TagAPI import TagAPI
from QnA.API.OrganizationAPI import OrganizationAPI
from QnA.API.LoginAPI import LoginAPI
from QnA.API.LogoutAPI import LogoutAPI
from QnA.API.VoteAPI import VoteAPI
from QnA.API.ResetPasswordAPI import ResetPasswordAPI

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', UserAPI.as_view()),

    url(r'^auth/login/?$', 'rest_framework.authtoken.views.obtain_auth_token', name="login"),
    url(r'^auth/load/?$', LoginAPI.as_view(), name="load"),
    url(r'^auth/logout/?$', LogoutAPI.as_view(), name="logout"),

    url(r'^answers/?$', AnswerAPI.as_view()),

    url(r'^comments/?$', CommentAPI.as_view()),

    url(r'^questions/(?P<question_id>[0-9]{1,9})/?$', QuestionAPI.as_view()),
    url(r'^questions/?$', QuestionAPI.as_view()),

    url(r'^tags/?$', TagAPI.as_view()),

    url(r'^organizations/(?P<organization_id>[0-9]{1,9})/?$', OrganizationAPI.as_view()),
    url(r'^organizations/?$', OrganizationAPI.as_view()),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^users/(?P<user_id>[0-9]{1,9})/?$', UserAPI.as_view()),
    url(r'^users/?$', UserAPI.as_view()),

    url(r'^votes/?$', VoteAPI.as_view()),

    url(r'^reset/?$', ResetPasswordAPI.as_view()),
)
