from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from pollstagram import views
from poll.models import Question
from taggit.models import Tag
from voting.views import vote_on_object

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.IndexView.as_view(), name='home'),
    url(r'^polls/$', views.IndexView.as_view(), name='polls_index'),
    url(r'^tags/$', views.ListView.as_view(model=Tag, context_object_name = 'tags'), name='tags_index'),
    # Generic view to vote on Link objects
    url(r'^polls/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', 
        vote_on_object, 
        dict(model=Question, template_object_name='questions', allow_xmlhttprequest=True)
    ),
    url(r'^answers/create/$', login_required(views.AnswerCreateView.as_view()), name='answer_create'),
    url(r'^polls/create/$', login_required(views.PollCreateView.as_view()), name='poll_create'),
    url(r'^polls/(?P<pk>\d+)/$', views.PollDetailView.as_view(), name='poll_detail'),
    url(r'^polls/(?P<pk>\d+)/results/$', login_required(views.PollResultsView.as_view()), name='poll_results'),
    url(r'^test/', TemplateView.as_view(template_name="test.html")),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Include django-registration views
    (r'^accounts/', include('registration.backends.default.urls')),

    # Display a user account
    url(r'^users/(?P<username>\w+)/$', views.PollDetailView.as_view()),
)
