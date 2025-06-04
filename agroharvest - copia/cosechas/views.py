from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Max, Min, Count
from datetime import timedelta
from django.utils import timezone
from .models import Sensor, LecturaSensor, Reporte, ConfiguracionAlertas
from .serializers import (
    SensorSerializer,
    LecturaSensorSerializer,
    ReporteSerializer,
    ConfiguracionAlertasSerializer
)
from .permissions import IsAdmin, IsAgricultor  # Custom permissions recomendadas

# --- Vistas Basadas en Funciones --- #
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])  # Mejor: Permission personalizada
def vista_para_admin(request):
    """Endpoint exclusivo para administradores"""
    return Response(
        {"mensaje": "Bienvenido, administrador"},
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAgricultor])
def vista_para_agricultor(request):
    """Endpoint exclusivo para agricultores"""
    return Response(
        {"mensaje": "Bienvenido, agricultor"},
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registrar_lectura(request, sensor_id):
    """
    Registra lectura y genera alertas automáticas
    """
    sensor = get_object_or_404(Sensor, id=sensor_id)
    
    try:
        valor = float(request.data['valor'])
    except (KeyError, ValueError):
        return Response(
            {"error": "Valor numérico requerido"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Crear lectura
    lectura = LecturaSensor.objects.create(
        sensor=sensor,
        valor=valor,
        usuario=request.user  # Registrar quién insertó la lectura
    )
    
    # Actualizar última lectura del sensor
    sensor.ultima_lectura = valor
    sensor.save()

    # Generar alerta si corresponde
    config = ConfiguracionAlertas.objects.first()
    if config and (valor < config.humedad_minima or valor > config.humedad_maxima):
        tipo = "BAJA" if valor < config.humedad_minima else "ALTA"
        Reporte.objects.create(
            titulo=f"Alerta de {sensor.get_tipo_display()} {tipo}",
            contenido=f"Sensor {sensor.nombre}: {valor} (Rango: {config.humedad_minima}-{config.humedad_maxima})",
            sensor=sensor,
            criticidad="ALTA" if tipo == "BAJA" else "MEDIA"
        )

    return Response(
        LecturaSensorSerializer(lectura).data,
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analizar_datos(request):
    """
    Análisis avanzado con agregaciones
    """
    fecha_inicio = timezone.now() - timedelta(days=7)
    
    datos = LecturaSensor.objects.filter(
        fecha__gte=fecha_inicio
    ).aggregate(
        promedio=Avg('valor'),
        maximo=Max('valor'),
        minimo=Min('valor'),
        total=Count('id')
    )

    return Response({
        "periodo": f"Datos desde {fecha_inicio.date()}",
        **datos
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_reportes(request):
    """
    Listado paginado de reportes
    """
    reportes = Reporte.objects.all().order_by('-fecha_creacion')
    serializer = ReporteSerializer(reportes, many=True)
    return Response({
        "count": reportes.count(),
        "results": serializer.data
    })

# --- Vistas Basadas en Clases --- #
class ConfiguracionAlertasView(generics.RetrieveUpdateAPIView):
    """
    GET/PUT de configuración de alertas
    """
    queryset = ConfiguracionAlertas.objects.all()
    serializer_class = ConfiguracionAlertasSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self):
        # Siempre trabaja con la primera configuración
        obj, _ = ConfiguracionAlertas.objects.get_or_create(pk=1)
        return obj

class SensorListView(generics.ListCreateAPIView):
    """
    Lista y crea sensores
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)