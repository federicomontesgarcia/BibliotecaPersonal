from rest_framework import serializers
from .models import Libro, Autor, Genero


class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ('nombre', 'precio', 'editorial', 'fecha', 'autor', 'genero')


class AutorSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=20)
    apellido = serializers.CharField(max_length=20)
    origen = serializers.CharField(max_length=30)
    nacimiento = serializers.DateField()

    class Meta:
        model = Autor
        fields = ('nombre', 'apellido', 'origen', 'nacimiento')


class GeneroSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=50)

    class Meta:
        model = Genero
        fields = ('__all__')


"""
class LibrosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libros
        fields = ('__all__')
"""
