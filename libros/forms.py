
from django import forms


class ActualizarLibroForm(forms.Form):
    isbn_libro = forms.CharField(label="ISBN del libro", required=True)
    titulo_libro = forms.CharField(label="Nombre del libro", required=True)
    autor_libro = forms.CharField(label="Autor del libro", required=True)
    anio_libro = forms.CharField(label="Año de publicación", required=True)


class ActualizarPaginaForm(forms.Form):
    texto_pagina = forms.CharField(
        label="Contenido de la página", required=True)


class BusquedaLibroForm(forms.Form):
    busqueda = forms.CharField(label="Busqueda", required=True)
