from rest_framework import serializers
from .models import Sensor, LecturaSensor, Reporte, UsuarioPersonalizado, ConfiguracionAlertas

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioPersonalizado
        fields = ['id', 'username', 'rol', 'email', 'telefono']

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'nombre', 'ubicacion', 'ultima_lectura']

class LecturaSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturaSensor
        fields = ['id', 'sensor', 'valor', 'fecha']

class ReporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporte
        fields = ['id', 'titulo', 'contenido', 'alerta', 'fecha_generacion']

class ConfiguracionAlertasSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionAlertas
        fields = '__all__'