from rest_framework import serializers
from .models import Consultas, Productos

#Creo el serializer para las consultas
class ConsultasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultas
        fields = '__all__'

# Creo el serializer para los productos
class ProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model =Productos
        fields = '__all__'