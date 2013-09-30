from django.http import HttpResponse
import os

def home(request):
    return HttpResponse(os.environ['AWS_STORAGE_BUCKET_NAME'])

