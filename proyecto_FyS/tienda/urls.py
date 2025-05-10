from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_tienda_fys, name='index'),
    path('sucursales/', views.sucursales, name='sucursales'), #agregue la urls para la pagina sucursales
]

