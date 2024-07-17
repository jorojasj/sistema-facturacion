from django import forms
from .models import *
from django.forms import inlineformset_factory


class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['nombre_cliente', 'compania', 'direccion', 'ciudad', 'estado_provincia', 'postal', 'telefono', 'numero_compra', 'nombre_producto', 'precio_producto', 'cantidad']


class MotivoRechazoForm(forms.ModelForm):
    class Meta:
        model = MotivoRechazo
        fields = ['motivo']


class Producto(models.Model):
    orden_compra = models.ForeignKey(OrdenCompra, related_name='productos', on_delete=models.CASCADE)
    nombre_producto = models.CharField(max_length=100)
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()

OrdenCompraProductoFormset = inlineformset_factory(
    OrdenCompra, Producto,
    fields=('nombre_producto', 'precio_producto', 'cantidad',),
    extra=2,  # Ajusta este valor según cuántos formularios quieres mostrar por defecto
    can_delete=True
)