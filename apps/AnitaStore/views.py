from django.shortcuts import render, redirect
from .models import *
import os 
from django.conf import settings
from django.http import HttpResponse
import json
from cryptography.fernet import Fernet
from sistemaFacturacion.settings import LLAVE_ENCRYPT

from django. contrib import messages


# Create your views here.
def cargarInicio(request):
    productos = Producto.objects.all()
    return render(request,"index.html",{"productos":productos})

