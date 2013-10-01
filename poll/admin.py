from django.contrib import admin
from django import forms 
from pagedown.widgets import AdminPagedownWidget
from poll.models import *

admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Vote)
admin.site.register(Answer)