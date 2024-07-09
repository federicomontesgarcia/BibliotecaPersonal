from django.shortcuts import render
from .models import Libro, Autor, Genero
import autores
from libros.models import Autor
from rest_framework import status
import requests
# Create your views here.


def autores(request):

    autores = Autor.objects.all()

    return render(request, "autores/autores.html", {"autores": autores})

