from django.contrib import admin
from django import forms 
from pagedown.widgets import AdminPagedownWidget
from poll.models import Tag, Question, Choice, Vote, Answer
from forms import QuestionForm

class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm

admin.site.register(Tag)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Vote)
admin.site.register(Answer)