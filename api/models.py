# api/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    usuario_id_sql = models.IntegerField(null=True, blank=True)
    
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Cambia el related_name para evitar conflictos
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Cambia el related_name para evitar conflictos
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )

    def __str__(self):
        return self.username

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Pago(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha_pago = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    concepto = models.CharField(max_length=200)

    def __str__(self):
        return f"Pago de {self.monto} a {self.empleado} el {self.fecha_pago}"
