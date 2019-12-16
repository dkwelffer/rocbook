from django import forms


class RapidOCRForm(forms.Form):
    # imagen = forms.FileField(label="Imagen", required=True)
    imagen = forms.ImageField(label='Imagen', required=True)


class CompletOCRForm(forms.Form):
    isbn_libro = forms.CharField(label="ISBN del libro", required=True)
    titulo_libro = forms.CharField(label="Nombre del libro", required=True)
    autor_libro = forms.CharField(label="Autor del libro", required=True)
    anio_libro = forms.CharField(label="Año de publicación", required=True)
    imagenes_libro = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=True)
