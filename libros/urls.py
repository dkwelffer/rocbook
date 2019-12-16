from django.urls import path

from . import views


app_name = 'libros'
urlpatterns = [
    path('', views.todos, name='todos'),
    path('<int:isbn>', views.libro, name='libro'),
    path('<int:isbn>/<int:numero>', views.pagina, name='pagina'),
    path('editar/<int:isbn>', views.editar_libro, name='editar_libro'),
    path('editar/<int:isbn>/<int:numero>', views.editar_pagina, name='editar_pagina'),
    path('buscar', views.buscar_libro, name="buscar")
]
