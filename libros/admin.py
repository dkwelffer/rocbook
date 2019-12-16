from django.contrib import admin

from .models import Libro, Pagina


admin.site.register(Libro)
admin.site.register(Pagina)