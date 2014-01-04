from django.conf.urls import patterns, include, url
from QnA.views import UserAPI

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', UserAPI.as_view()),
    #url(r'^$', 'Kiitti.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
