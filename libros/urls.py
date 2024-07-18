from django.urls import include, path

from . import views

urlpatterns = [
    #path('', views.autores, name="Autores"),
    path('', views.libros, name="Libros"),
    path('save-book', views.save_book, name="grabarLibro"),
    path('biblioteca', views.biblioteca, name="Biblioteca"),
]
