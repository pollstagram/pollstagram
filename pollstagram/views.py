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
    if 'search' in request.GET and 'keyword' in request.GET:
        keyword = request.GET['keyword']
        results = Question.objects.filter(content_rawtext__icontains = keyword)
    else:
        results =  Question.objects.all()
    return render(request, 'list.html', {'questions': results,})