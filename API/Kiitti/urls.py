from django.conf.urls import patterns, include, url
from QnA.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', UserAPI.as_view()),
    #url(r'^$', 'Kiitti.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^answers/?$', AnswerAPI.as_view()),
    url(r'^comments/?$', CommentAPI.as_view()),
    url(r'^questions/(?P<style>latest|hottest)/?$', QuestionAPI.as_view()),
    url(r'^questions/?$', QuestionAPI.as_view()),
    url(r'^tags/?$', TagAPI.as_view()),
    url(r'^organizations/?$', OrganizationAPI.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
