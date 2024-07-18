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


#-------------
class LibroViews(APIView):
    serializer_class = LibroSerializer

    def get_queryset(self):
        return Libro.objects.all()

    def post(self, request):
        print("entra en post")
        print(request.data)
        serializer = LibroSerializer(data=request.data)

        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, id=None):
        if id:
            item = Libro.objects.get(id=id)
            print("libro")
            print(item)
            serializer = LibroSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = Libro.objects.all()
        serializer = LibroSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, id=None):
        item = Libro.objects.get(id=id)
        serializer = LibroSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        item = get_object_or_404(Libro, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})


class AutorViews(APIView):
    serializer_class = AutorSerializer

    def get_queryset(self):
        return Autor.objects.all()

    def post(self, request):
        serializer = AutorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, id=None):
        if id:
            item = Autor.objects.get(id=id)
            serializer = AutorSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = Autor.objects.all()
        serializer = AutorSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, id=None):
        item = Autor.objects.get(id=id)
        serializer = AutorSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        item = get_object_or_404(Autor, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})


class GeneroViews(APIView):
    serializer_class = GeneroSerializer

    def get_queryset(self):
        return Genero.objects.all()

    def post(self, request):
        serializer = GeneroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, id=None):
        if id:
            item = Genero.objects.get(id=id)
            print("item")
            print(item)
            serializer = GeneroSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = Genero.objects.all()
        serializer = GeneroSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, id=None):
        item = Genero.objects.get(id=id)
        serializer = GeneroSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        item = get_object_or_404(Genero, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})


#--- GOOGLE API BOOKS ---

class LibrosViews(APIView):

    def get(self, request, clave_api='AIzaSyCIUpw80bNcmyZZmVemB49yQcrViWjVvjs'):
        print("entra en Libros Views")
        titulo = "el fin de la eternidad isaac asimov"
        url = f"https://www.googleapis.com/books/v1/volumes?q={titulo}&key={clave_api}"
        print("url")
        print(url)

        try:
            response = requests.get(url)
            response.raise_for_status()  # Si la solicitud no es exitosa, lanzará una excepción
            data = response.json()

            for datos in data['items']:

                titulo = datos['volumeInfo']['title']
                autor = datos['volumeInfo'].get('authors', ['Desconocido'])
                fecha = datos['volumeInfo'].get('publishedDate', ['Desconocida'])
                paginas = datos['volumeInfo'].get('pageCount', ['Desconocida'])
                descripcion = datos['volumeInfo'].get('description', ['Desconocida'])
                if 'imageLinks' in datos['volumeInfo']:
                    imagen = datos['volumeInfo']['imageLinks'].get('thumbnail', 'Desconocida')
                else:
                    imagen = 'Desconocida'

                print(f"Título: {titulo}")
                print(f"Autor: {autor}")
                print(f"Fecha de publicación: {fecha}")
                print(f"Número de páginas: : {paginas}")
                print(f"Descripción: {descripcion}")
                print(f"Imagen: {imagen}")

            return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            print("Error al realizar la solicitud:", e)
            return Response({"status": "error", "status":status.HTTP_400_BAD_REQUEST})


