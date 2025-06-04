from django.core.management.base import BaseCommand
from cosechas.models import Sensor
import random
import time

#elbasecomand activa un comando tipo manage.py
class Command(BaseCommand):
    help = 'Simula lecturas de sensores IoT'

    def handle(self, *args, **options):
        sensor = Sensor.objects.create(nombre="Sensor-1", ubicacion="Invernadero A")
        
        while True:
            valor = random.uniform(20.0, 80.0)  # Humedad aleatoria
            self.stdout.write(f"Enviando lectura: {valor}%")
            
            # Registrar lectura (simulando POST a la API)
            from cosechas.views import registrar_lectura
            from rest_framework.test import APIRequestFactory
            
            factory = APIRequestFactory()
            request = factory.post(
                f'/api/sensores/{sensor.id}/lecturas/',
                {'valor': valor},
                format='json'
            )
            registrar_lectura(request, sensor.id)
            
            time.sleep(10)  # Espera 10 segundos