from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Sensor, LecturaSensor, Reporte
from .serializers import SensorSerializer, LecturaSensorSerializer, ReporteSerializer
from datetime import timedelta
from django.utils import timezone

@api_view(['POST'])
def registrar_lectura(request, sensor_id):
    """Registra una lectura de humedad desde un sensor IoT"""
    sensor = Sensor.objects.get(id=sensor_id)
    valor = request.data.get('valor')

    # Guardar lectura
    lectura = LecturaSensor.objects.create(sensor=sensor, valor=valor)
    sensor.ultima_lectura = valor
    sensor.save()

    # Generar reporte si la humedad es crítica
    if valor < 30.0 or valor > 70.0:
        Reporte.objects.create(
            titulo=f"Alerta de humedad en {sensor.nombre}",
            contenido=f"Valor crítico: {valor}%",
            alerta=True
        )
    else :
        Reporte.objects.create(
            titulo=f"Registro de humedad en {sensor.nombre}",
            contenido=f"Valor normal: {valor}%",
            alerta=False
        )
        

    return Response({"status": "Lectura registrada"}, status=201)

@api_view(['GET'])
def analizar_datos(request):
    """Analiza lecturas de los últimos 7 días"""
    fecha_inicio = timezone.now() - timedelta(days=7)
    lecturas = LecturaSensor.objects.filter(fecha__gte=fecha_inicio)
    
    # Cálculo básico (promedio)
    promedio = sum([l.valor for l in lecturas]) / len(lecturas) if lecturas else 0

    return Response({
        "promedio_humedad": promedio,
        "total_lecturas": len(lecturas)
    })

@api_view(['GET'])
def listar_reportes(request):
    """Lista todos los reportes generados"""
    reportes = Reporte.objects.all()
    serializer = ReporteSerializer(reportes, many=True)
    return Response(serializer.data)