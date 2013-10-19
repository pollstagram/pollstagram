from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

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
    url(r'^polls/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', 
        vote_on_object, 
        dict(model=Question, template_object_name='questions', allow_xmlhttprequest=True)
    ),
    url(r'^answers/create/$', login_required(views.AnswerCreateView.as_view()), name='answer_create'),
    url(r'^test/', TemplateView.as_view(template_name="nav_test.html")),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Include django-registration views
    (r'^accounts/', include('registration.backends.default.urls')),
)
