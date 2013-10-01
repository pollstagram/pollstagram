from django.http import HttpResponse
from django.shortcuts import render
from poll.models import Question

def home(request):
    return render(request, 'list.html', {'questions': Question.objects.all(),})

