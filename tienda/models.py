from django.db import models
from django.contrib.auth.models import User
import secrets
from datetime import datetime, timedelta
from django.utils import timezone

# Tabla consulta
class Consultas(models.Model):
    #Columnas de la DB
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    telefono = models.CharField(max_length=25)
    categoria_detectada = models.CharField(max_length=50, blank=True)
    mensaje = models.TextField()

    class Meta:
        db_table = 'consultas'

# Tabla Productos (Colecciones)
class Productos(models.Model):

    # Choices para el tipo de coleccion
    tipos = [
        ('1', 'Pantalon'),
        ('2','Remera'),
        ('3','Top'),
        ('4','Vestido'),
        ('5','Buzo'),
        ('6','Campera'),
        ('7','Accesorio')
    ]

    # Columnas de la DB
    nombre = models.CharField(max_length=100, unique = True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(default="Sin descripción")
    tipo = models.CharField(max_length=1, choices=tipos)
    imagen = models.ImageField(upload_to='prendas/', null=True, blank=True)

    class Meta:
        db_table = 'productos'

#Funcion para generar codigo aleatorio
def generar_codigo(longitud=6):
    return ''.join(secrets.choice('0123456789') for _ in range(longitud))

#Funcion para la expiracion del codigo luego de 10 minutos
def expiracion_codigo():
    return timezone.now() + timedelta(minutes=1)

#Modelo codigo de validacion
class CodigoValidacion(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE) #Usuario Django
    codigo = models.CharField(max_length=6, default=generar_codigo) #Codigo con la funcion
    creado = models.DateTimeField(auto_now_add=True) #Fecha y hora que se creo el primer codigo
    expiracion = models.DateTimeField(default=expiracion_codigo) #Expiracion en 10 minutos
    usado = models.BooleanField(default=False) #Detecta si fue usado o no

    #Validacion si fue usado o no
    def es_valido(self):
        return not self.usado and timezone.now() <= self.expiracion