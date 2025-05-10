from django.db import models

# Create your models here.
class usuario(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    telefono = models.IntegerField(max_length=50)
    password = models.CharField(max_length=50)
    rol = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre