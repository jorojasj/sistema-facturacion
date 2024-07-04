from django import forms
from .models import *


class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['nombre_cliente', 'compania', 'direccion', 'ciudad', 'estado_provincia', 'postal', 'telefono', 'numero_compra', 'nombre_producto', 'precio_producto', 'cantidad']


class MotivoRechazoForm(forms.ModelForm):
    class Meta:
        model = MotivoRechazo
        fields = ['motivo']