
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from libros.models import Libro, Pagina

from principal.views import get_name
from .forms import CompletOCRForm, RapidOCRForm
from .utils import extract_text, save_simple_image


@login_required
def rapido(request):

    name = get_name(request)

    if request.method == 'POST':
        form = RapidOCRForm(request.POST, request.FILES)

        if form.is_valid():
            filename = save_simple_image(request.FILES['imagen'])

            text = extract_text(filename)

            context = {
                'resultado': text,
                'name': name
                }

            return render(request, 'ocr/rapido.html', context)

        else:
            msg = 'Error de formulario, revise los datos suministrados e ' +\
                'intente de nuevo'
            context = {
                'error': msg,
                'name': name
            }
            return render(request, 'ocr/rapido.html', context)

    else:
        return render(request, 'ocr/rapido.html', {'name': name})


@login_required
def completo(request):

    if request.method == 'POST':
        form = CompletOCRForm(request.POST, request.FILES)

        if form.is_valid():

            libro = Libro(
                isbn=form.cleaned_data['isbn_libro'],
                titulo=form.cleaned_data['titulo_libro'],
                autor=form.cleaned_data['autor_libro'],
                anio=form.cleaned_data['anio_libro']
            )
            libro.save()

            images = request.FILES.getlist('imagenes_libro')

            for i, image in enumerate(sorted(images, key=lambda f: f.name)):
                Pagina.objects.create(
                    libro=libro,
                    numero=i + 1,
                    imagen=image
                )

            name = get_name(request)

            context = {
                'resultado': True,
                'name': name
            }

            return render(request, 'ocr/completo.html', context)

        errors = form.errors
        name = get_name(request)
        context = {
            'errors': errors,
            'name': name
        }
        return render(request, 'ocr/completo.html', context)

    else:
        form = CompletOCRForm()
        name = get_name(request)
        context = {
            'form': form,
            'name': name
        }
        return render(request, 'ocr/completo.html', context)
