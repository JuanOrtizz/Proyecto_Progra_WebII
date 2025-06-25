from django.db import models

# Create your models here.

# Tabla consulta
class Consultas(models.Model):
    #Columnas de la DB
    nombre = models.CharField(max_length=100)
    email = models.CharField(max_length=320)
    telefono = models.CharField(max_length=25)
    categoria_detectada = models.CharField(max_length=50, blank=True)
    mensaje = models.TextField()

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
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=tipos)
    imagen = models.ImageField(upload_to='prendas/', null=True, blank=True)

    class Meta:
        db_table = 'Productos'

#Tabla Usuarios Permitidos
class UsuariosPermitidos(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    codigo_validacion = models.CharField(max_length=6)