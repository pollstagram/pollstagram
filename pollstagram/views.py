from django.http import HttpResponse
from django.shortcuts import render
from poll.models import Question
from django.views import generic
import os

class IndexView(generic.ListView):
    model = Question
    template_name = 'list.html'
    context_object_name = 'questions'

def home(request):
    return render(request, 'list.html', {'questions': Question.objects.all(),})