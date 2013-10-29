from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from pollstagram import views
from poll.models import Question
from taggit.models import Tag
from voting.views import vote_on_object

from poll.forms import UserProfileForm, UserEditForm
from registration.backends.default.views import RegistrationView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.IndexView.as_view(), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^polls/$', views.IndexView.as_view(), name='polls_index'),
    url(r'^tags/$', views.ListView.as_view(model=Tag, context_object_name = 'tags'), name='tags_index'),
    # section 2.3 of RFC 3986 safe and unreserverd url
    url(r'^tags/(?P<tag>[\w\+\-\.\_\~]+)/$', views.IndexView.as_view(), name='tags_questions'),
    # Generic view to vote on Link objects
    url(r'^polls/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', 
        vote_on_object, 
        dict(model=Question, template_object_name='questions', allow_xmlhttprequest=True)
    ),
    url(r'^answers/create/$', login_required(views.AnswerCreateView.as_view(), redirect_field_name=None), name='answer_create'),
    url(r'^polls/create/$', login_required(views.PollCreateView.as_view()), name='poll_create'),
    url(r'^polls/(?P<pk>\d+)/$', views.PollDetailView.as_view(), name='poll_detail'),
    url(r'^polls/(?P<pk>\d+)/delete$', views.PollDeleteView.as_view(), name='poll_delete'),
    url(r'^polls/(?P<pk>\d+)/edit/$', login_required(views.PollUpdateView.as_view()), name='poll_update'),
    url(r'^polls/(?P<pk>\d+)/revisions/$', views.PollRevisionDetailView.as_view(), name='poll_revisions'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Include django-registration views
    # Custom user registration entry must appear BEFORE
    # default
    url(r'accounts/register/$', 
            RegistrationView.as_view(form_class = UserProfileForm), 
	            name = 'registration_register'),
    (r'^accounts/', include('registration.backends.default.urls')),

    # Display a user account
    url(r'^users/(?P<slug>\w+)/$', views.UserDetailView.as_view(), name='user_detail'),
    url(r'^users/$', views.UserListView.as_view(), name='user_list'),

    # Edit profile page
    url(r'^users/(?P<slug>\w+)/edit/$', login_required(views.UserUpdateView.as_view()), name='user_edit'),
)
