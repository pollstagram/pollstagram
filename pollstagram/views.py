from django.http import HttpResponse
from django.shortcuts import render
from poll.models import Question
import os

def home(request):
    if 'search' in request.GET and 'keyword' in request.GET:
        keyword = request.GET['keyword']
        results = Question.objects.filter(content_rawtext__icontains = keyword)
    else:
        results =  Question.objects.all()
    return render(request, 'list.html', {'questions': results,})