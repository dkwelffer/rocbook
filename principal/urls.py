from django.urls import path
from . import views


app_name = 'principal'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_session, name='login'),
    path('logout', views.logout_session, name='logout')
]