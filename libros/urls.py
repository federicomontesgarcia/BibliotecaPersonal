from django.urls import include, path

from . import views

urlpatterns = [
    #path('', views.autores, name="Autores"),
    path('', views.libros, name="Libros"),
    path('', views.LibroViews.as_view(), name="libro"),
    path('save-book', views.save_book, name="grabarLibro"),


    path('libro/<int:id>/', views.LibroViews.as_view()),
    path('autor/', views.AutorViews.as_view(), name="autor"),
    path('autor/<int:id>/', views.AutorViews.as_view()),
    path('genero/', views.GeneroViews.as_view()),
    path('genero/<int:id>/', views.GeneroViews.as_view(), name="genero"),
    path('books/', views.LibrosViews.as_view(), name="books"),
    #path('popular/', views.libroMasPopular.as_view(), name='popular'),
]
