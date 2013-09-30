from django.http import HttpResponse
import os

def home(request):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    files = [f for f in os.listdir(cur_dir)]
    return HttpResponse('\n'.join(files))

