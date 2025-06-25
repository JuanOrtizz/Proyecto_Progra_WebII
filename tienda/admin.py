from django.contrib import admin
from .models import Consultas, Productos, UsuariosPermitidos

admin.site.register([Consultas, Productos, UsuariosPermitidos]) # Registro el modelo Consultas y Productos en admin