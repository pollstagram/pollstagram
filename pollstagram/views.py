from django.http import HttpResponse
from django.shortcuts import render
import os

def home(request):
    return render(request, 'base.html')
    # cur_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # files = [f for f in os.listdir(cur_dir)]
    # return HttpResponse('\n'.join(files))

