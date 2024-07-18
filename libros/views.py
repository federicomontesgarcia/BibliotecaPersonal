from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.templatetags.rest_framework import data
from rest_framework.views import APIView
from .serializers import LibroSerializer, AutorSerializer, GeneroSerializer
from .models import Libro, Autor, Genero
import requests
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.shortcuts import render
from libros.models import Libro

# Create your views here.

def __get_libros():
    url = 'http://localhost:8000/libros/v1'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()

    return []


def libros(request):
    libros = __get_libros()
    libros = libros['data']['data']
    
    i = 0
    for row in libros:
        id = row['id']
        nombre = row['nombre']
        autor = row['autor']
        
        autor = autor.split()
        nombreAutor = autor[0]
        apellidoAutor = autor[1]
        codigoAutor = Autor.objects.filter(nombre = nombreAutor, apellido = apellidoAutor).values('id')
        codigoAutor = list(codigoAutor)
        autorId = codigoAutor[0]['id']

        libroExiste = Libro.objects.filter(nombre = nombre, autor = autorId)
        
        flag = ""
        if libroExiste:
            flag = '1'
        else:
            flag = '0'
        
        libros[i]['flag'] = flag
        i = i + 1
    
    return render(request, "libros/libros.html", {
        'libros': libros
    })


@api_view(["POST"])
@permission_classes((AllowAny,))
def save_book(request):
    """function to save books."""

    if request.method == 'POST':
        
        try:
            data = request.data  # Accede directamente a los datos enviados en la solicitud POST
            
            button_value = data['button']

            index = data.getlist('id').index(button_value)

            id_value = data.getlist('id')[index]
            book_name = data.getlist('bookName')[index]
            
            author = data.getlist('author')[index]

            author = author.split()
            authorName = author[0]
            authorLastName = author[1]
            authorId = Autor.objects.filter(nombre=authorName, apellido=authorLastName).values('id')
            authorId = authorId[0]
            authorId = authorId['id']
            
            gender = data.getlist('gender')[index]

            genderId = Genero.objects.filter(nombre=gender).values('id')
            genderId = genderId[0]
            genderId = genderId['id']

            editorial = data.getlist('editorial')[index]
            year = data.getlist('year')[index]
            price = data.getlist('price')[index]
            price = price

            price_str = price

            try:
                price = Decimal(price_str.replace(',', '.'))
            
            except ValueError:
                precio = None  
                    
            try:
                authorName = Autor.objects.get(id=authorId)
                genderName = Genero.objects.get(id=genderId)
            
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Autor o Género no encontrado'}, status=400)
            
            libro = Libro(
                nombre = book_name,
                autor_id = authorId,
                genero_id = genderId,
                editorial = editorial,
                fecha = year,
                precio = price
                #imagen = image
            )
            libro.save()

            messages.success(request, 'El libro se agregó satisfactoriamente.')
            return redirect('Libros')
        
        except Exception as e:
            return JsonResponse({'error': 'Error al procesar los datos'}, status=400)
    
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


#--- Listado de libros en la vista ---

def biblioteca(request):
    """Función para mostrar la información de los libros"""

    libros = Libro.objects.all()

    return render(request, "libros/biblioteca.html", {"libros": libros})


