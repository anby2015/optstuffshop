# Create your views here.
from django.http import HttpResponse

def details(request):
    return HttpResponse("Hello world")
