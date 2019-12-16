
from ocr.utils import extract_text
from os import environ
from time import sleep
import multiprocessing

# Configuracion de django
import django
environ.setdefault('DJANGO_SETTINGS_MODULE', 'librocr.settings')
django.setup()

# No se pueden inportar los modelos antes de la configuracion de Django
from libros.models import Libro, Pagina


def procesar_pagina(pagina):

    print("[Servidor ROC] Pagina {actual}".format(actual=pagina.numero))
    texto = extract_text(pagina.imagen.path)
    pagina.texto = texto
    pagina.save()


def procesar_libro(libro):

    print("[Servidor ROC] Procesando libro {titulo}".format(
        titulo=libro.titulo))
    paginas = Pagina.objects.filter(libro=libro)

    with multiprocessing.Pool() as pool:
        pool.map(procesar_pagina, paginas)

    libro.procesado = True
    libro.save()

    print("[Servidor ROC] Libro {titulo} procesado correctamente.".format(
        titulo=libro.titulo))


def proceso_roc():

    print("[Servidor ROC] Iniciando...")

    while True:
        libros = Libro.objects.filter(procesado=False)

        if len(libros):
            print("[Servidor ROC] Hay libros sin procesar.")

            for libro in libros:
                procesar_libro(libro)
        else:
            sleep(5)


if __name__ == '__main__':
    proceso_roc()
