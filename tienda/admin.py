from django.contrib import admin
from .models import Consultas, Productos, CodigoValidacion

admin.site.register([Consultas, Productos, CodigoValidacion]) # Registro el modelo Consultas y Productos en admin