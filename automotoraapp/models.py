from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now

class Vehiculo(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    año = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(now().year)]
    )
    color = models.CharField(max_length=50)
    precio = models.DecimalField(
        max_digits=12, decimal_places=0,
        validators=[MinValueValidator(0)]
    )
    kilometraje = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )
    tipo_combustible = models.CharField(
        max_length=50,
        choices=[
            ('gasolina', 'Gasolina'),
            ('diesel', 'Diesel'),
            ('electrico', 'Eléctrico'),
            ('hibrido', 'Híbrido'),
        ]
    )
    transmision = models.CharField(
        max_length=50,
        choices=[
            ('manual', 'Manual'),
            ('automatica', 'Automática'),
        ]
    )
    numero_puertas = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(5)]
    )
    fecha_registro = models.DateField(auto_now_add=True)
