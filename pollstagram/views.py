from django.http import HttpResponse

def home(request):
    return HttpResponse(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

