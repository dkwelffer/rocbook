from django.db import models


class Libro(models.Model):
    isbn = models.CharField(max_length=24, primary_key=True, default='x')
    titulo = models.CharField(max_length=120, default='x')
    autor = models.CharField(max_length=120, default='x')
    anio = models.CharField(max_length=4, default='x')

    procesado = models.BooleanField(default=False)
    estado = models.BooleanField(default=True)

    def cantidad_paginas(self):
        return len(Pagina.objects.filter(libro=self))

    def __str__(self):
        return self.isbn + ' - ' + self.titulo


class Pagina(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    numero = models.IntegerField()
    imagen = models.ImageField(upload_to='paginas')
    texto = models.CharField(max_length=5000, blank=True, default='')

    def anterior(self):
        if self.numero > 1:
            return self.numero - 1
        return None

    def siguiente(self):
        if self.numero < len(Pagina.objects.filter(libro=self.libro)):
            return self.numero + 1
        return None

    def navegacion(self):
        lista = None
        if 1 < self.numero < len(Pagina.objects.filter(libro=self.libro)):
            lista = [i for i in range(self.numero - 1, self.numero + 2)]
        elif self.numero == 1:
            lista = [1, 2, 3]
        elif self.numero == len(Pagina.objects.filter(libro=self.libro)):
            lista = [i for i in range(self.numero - 2, self.numero + 1)]
        return lista

    def __str__(self):
        return '{libro} - pagina {numpagina}'.format(
            libro=self.libro.titulo,
            numpagina=self.numero
        )
