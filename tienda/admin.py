from django.contrib import admin
from .models import Consultas, Productos

admin.site.register([Consultas, Productos]) # Registro el modelo Consultas y Productos en admin