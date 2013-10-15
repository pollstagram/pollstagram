from django.conf.urls import patterns, include, url

from pollstagram import views
from poll.models import Question
from voting.views import vote_on_object

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.IndexView.as_view(), name='home'),
    # Generic view to vote on Link objects
    url(r'^polls/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', vote_on_object, dict(model=Question, template_object_name='questions', allow_xmlhttprequest=True)),
    
    # url(r'^pollstagram/', include('pollstagram.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
