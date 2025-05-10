from rest_framework import serializers
from app_prueba.models import usuario 
class usuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = usuario
        fields = ['id', 'password', 'rol','nombre', 'email', 'telefono', 'direccion']