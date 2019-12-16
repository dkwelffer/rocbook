from django.urls import path

from . import views


app_name = 'ocr'
urlpatterns = [
    path('rapido', views.rapido, name='rapido'),
    path('completo', views.completo, name='completo'),
]