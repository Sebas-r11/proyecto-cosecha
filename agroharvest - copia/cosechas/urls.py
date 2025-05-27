from django.urls import path
from .views import (
    registrar_lectura,
    analizar_datos,
    listar_reportes
)

urlpatterns = [
    path('sensores/<int:sensor_id>/lecturas/', registrar_lectura, name='registrar_lectura'),
    path('analisis/', analizar_datos, name='analizar_datos'),
    path('reportes/', listar_reportes, name='listar_reportes'),
]