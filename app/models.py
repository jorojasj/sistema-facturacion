from django.db import models

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
    # Nuevo campo estado
    ESTADOS = (
        ('creada', 'Creada'),
        ('rectificada', 'Rectificada'),
    )
    estado = models.CharField(max_length=11, choices=ESTADOS, default='creada')

    def __str__(self):
        txt = "Codigo: {0} - Nombre Cliente: {1} - Compañia: {2}"
        return txt.format(self.numero_compra, self.nombre_cliente, self.compania)



class Entrega(models.Model):
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
    pass

class MotivoRechazo(models.Model):
    entrega = models.ForeignKey(Entrega, on_delete=models.CASCADE, related_name='motivos_rechazo')
    motivo = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rechazado el {self.fecha.strftime('%Y-%m-%d %H:%M')}: {self.motivo}"