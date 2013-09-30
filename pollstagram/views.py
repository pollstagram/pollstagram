from django.http import HttpResponse
import os

def home(request):
    return HttpResponse(os.path.abspath(__file__))

