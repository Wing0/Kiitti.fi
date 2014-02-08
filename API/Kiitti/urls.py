from django.conf.urls import patterns, include, url
from QnA.AnswerAPI import AnswerAPI
from QnA.UserAPI import UserAPI
from QnA.CommentAPI import CommentAPI
from QnA.QuestionAPI import QuestionAPI
from QnA.TagAPI import TagAPI
from QnA.OrganizationAPI import OrganizationAPI
from QnA.LoginAPI import LoginAPI
from QnA.LogoutAPI import LogoutAPI
from QnA.VoteAPI import VoteAPI
from QnA.ResetPasswordAPI import ResetPasswordAPI

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', UserAPI.as_view()),
    url(r'^auth/login/?$', LoginAPI.as_view()),
    url(r'^auth/logout/?$', LogoutAPI.as_view()),
    # url(r'^$', 'Kiitti.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^answers/?$', AnswerAPI.as_view()),
    url(r'^comments/?$', CommentAPI.as_view()),
    url(r'^questions/(?P<style>latest|hottest)/?$', QuestionAPI.as_view()),
    url(r'^questions/?$', QuestionAPI.as_view()),
    url(r'^tags/?$', TagAPI.as_view()),
    url(r'^organizations/?$', OrganizationAPI.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/?$', UserAPI.as_view()),
    url(r'^votes/?$', VoteAPI.as_view()),
    url(r'^reset/?$', ResetPasswordAPI.as_view()),
)
