from django.contrib import admin
from .models import Libro, Autor, Genero

# Register your models here.

admin.site.register(Libro)

admin.site.register(Autor)

admin.site.register(Genero)