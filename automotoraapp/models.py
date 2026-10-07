from django.db import models

# Create your models here.

class Auto(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    año = models.IntegerField()
    color = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=20, decimal_places=0)
    kilometraje = models.IntegerField()
    tipo_combustible = models.CharField(max_length=50, choices=[
        ('gasolina', 'Gasolina'),
        ('diesel', 'Diesel'),
        ('electrico', 'Electrico'),
        ('hibrido', 'Hibrido'),
    ])
    transmision = models.CharField(max_length=50, choices=[
        ('manual', 'Manual'),
        ('automatica', 'Automatica'),
    ])
    numero_de_puertas = models.IntegerField()
    fecha_de_registro = models.DateField(auto_now_add=True)