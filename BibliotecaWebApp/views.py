from django.shortcuts import render, HttpResponse
from django.conf import settings

# Create your views here.

def home(request):

    return render(request, "BibliotecaWebApp/home.html")






