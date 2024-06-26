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
    numero_compra = models.IntegerField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    precio_producto = models.IntegerField()
    cantidad = models.IntegerField()

    def __str__(self):
        txt = "Codigo: {0} - Nombre Cliente: {1} - Compañia: {2}"
        return txt.format(self.numero_compra, self.nombre_cliente, self.compania)


