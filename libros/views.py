from django.shortcuts import render, get_object_or_404, Http404
from django.contrib.auth.decorators import login_required

from principal.views import get_name
from .models import Libro, Pagina
from .forms import ActualizarLibroForm, ActualizarPaginaForm, BusquedaLibroForm


# Funciones auxiliares
def get_libro_or_404(isbn):

    try:
        _libro = Libro.objects.get(isbn=isbn)
        return _libro
    except Libro.DoesNotExist:
        raise Http404


# Vistas
@login_required
def todos(request):

    libros = Libro.objects.filter(estado=True)
    name = get_name(request)
    context = {
        'libros': libros,
        'name': name
    }
    return render(request, 'libros/todos.html', context)


@login_required
def libro(request, isbn, altcontext={}):

    libro_object = get_object_or_404(Libro, isbn=isbn)
    name = get_name(request)
    context = {
        'libro': libro_object,
        'name': name
        }
    context.update(altcontext)
    return render(request, 'libros/libro.html', context)


@login_required
def pagina(request, isbn, numero, altcontext={}):

    _libro = get_libro_or_404(isbn)
    pagina_object = get_object_or_404(Pagina, libro=_libro, numero=numero)
    name = get_name(request)

    context = {
        'libro': _libro,
        'pagina': pagina_object,
        'name': name
        }
    context.update(altcontext)

    return render(
        request,
        'libros/pagina.html',
        context
    )


@login_required
def editar_libro(request, isbn):

    actualizo = False

    if request.method == 'POST':
        form = ActualizarLibroForm(request.POST)

        if form.is_valid():
            _libro = get_libro_or_404(isbn=form.cleaned_data['isbn_libro'])
            _libro.titulo = form.cleaned_data['titulo_libro']
            _libro.autor = form.cleaned_data['autor_libro']
            _libro.anio = form.cleaned_data['anio_libro']
            _libro.save()
            response = libro(request, isbn, {'actualizo': True})
            return response

    _libro = get_object_or_404(Libro, isbn=isbn)
    name = get_name(request)
    context = {
        'libro': _libro,
        'actualizo': actualizo,
        'name': name
        }
    return render(
        request,
        'libros/editar_libro.html',
        context)


@login_required
def editar_pagina(request, isbn, numero):

    if request.method == 'POST':
        _form = ActualizarPaginaForm(request.POST)
        
        if _form.is_valid():
            _libro = get_libro_or_404(isbn)
            _pagina = get_object_or_404(Pagina, libro=_libro, numero=numero)

            _pagina.texto = _form.cleaned_data['texto_pagina']
            _pagina.save()

            response = pagina(request, isbn, numero, {'actualizo': True})
            return response

    _libro = get_libro_or_404(isbn)
    _pagina = get_object_or_404(Pagina, libro=_libro, numero=numero)
    name = get_name(request)
    context = {
        'libro': _libro,
        'pagina': _pagina,
        'name': name
    }
    return render(request, 'libros/editar_pagina.html', context)


@login_required
def buscar_libro(request):

    _form = BusquedaLibroForm(request.GET)
    if _form.is_valid():

        busqueda = request.GET['busqueda']
        _paginas = Pagina.objects.filter(texto__icontains=busqueda)
        resultados = []

        for _pag in _paginas:
            resultados.append(
                {
                    'libro': _pag.libro.titulo,
                    'isbn': _pag.libro.isbn,
                    'pagina': _pag.numero
                })

        return render(
            request,
            'libros/buscar_libro.html',
            {
                'resultados': resultados,
                'name': get_name(request)
            })

    return render(
        request,
        'libros/buscar_libro.html',
        {'name': get_name(request)}
    )
