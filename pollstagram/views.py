from django.http import HttpResponse

def home(request):
    return HttpResponse("HERRO from django, try out <a href='/admin/'>/admin/</a>\n")

