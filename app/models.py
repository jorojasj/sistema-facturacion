from django.db import models

# Create your models here.

class OrdenCompra(models.Model):
    nombre_cliente = models.CharField(max_length=100)
    compania = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    estado_provincia = models.CharField(max_length=100)
    postal = models.IntegerField()
    telefono = models.IntegerField()
    numero_compra = models.IntegerField(unique=True)
    nombre_producto = models.CharField(max_length=100)
    precio_producto = models.IntegerField()
    cantidad = models.IntegerField()


