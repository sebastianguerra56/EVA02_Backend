from django.urls import path
from . import views


urlpatterns = [
    path('', views.inicio, name= 'inicio'),
    path('crear/', views.crear_auto, name='crear_auto'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('ver/<int:auto_id>/', views.ver_auto, name='ver_auto'),
]