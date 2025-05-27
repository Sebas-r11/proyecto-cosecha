from rest_framework import serializers
from .models import Sensor, LecturaSensor, Reporte

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