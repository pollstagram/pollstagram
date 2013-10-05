from django.http import HttpResponse
from django.shortcuts import render
from poll.models import Question
import os

def home(request):
    return render(request, 'list.html', {'questions': Question.objects.all(), 'env', os.environ,})

