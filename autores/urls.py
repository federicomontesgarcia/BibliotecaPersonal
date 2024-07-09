from django.urls import path

from . import views


urlpatterns = [
    path('', views.autores, name="Autores"),
]
