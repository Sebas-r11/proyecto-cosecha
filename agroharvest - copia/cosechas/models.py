from django.contrib.auth.models import AbstractUser
from django.db import models

class UsuarioPersonalizado(AbstractUser):
    # Roles disponibles
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        AGRICULTOR = 'AGRICULTOR', 'Agricultor'

    rol = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.AGRICULTOR  # Valor por defecto
    )

    # Campos adicionales (opcionales)
    telefono = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"

class Sensor(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    ultima_lectura = models.FloatField(default=0.0)  # Humedad registrada
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.ubicacion})"

class LecturaSensor(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    valor = models.FloatField()  # Humedad (%)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor.nombre}: {self.valor}%"

class Reporte(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    alerta = models.BooleanField(default=False)  # True si hay valores críticos

    def __str__(self):
        return self.titulo
    
class ConfiguracionAlertas(models.Model):
    humedad_minima = models.FloatField(default=30.0, verbose_name="Humedad Mínima Aceptable (%)")
    humedad_maxima = models.FloatField(default=70.0, verbose_name="Humedad Máxima Aceptable (%)")
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuración de Alertas"
        verbose_name_plural = "Configuraciones de Alertas"

    def __str__(self):
        return f"Límites: {self.humedad_minima}%-{self.humedad_maxima}%"