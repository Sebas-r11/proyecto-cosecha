from django.db import models

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