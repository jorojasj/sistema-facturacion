from io import BytesIO
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import *
#IMPORTS DEL PDF
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# Create your views here.
def index(request):
    return render(request,"index.html")

def cargarLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def cargarLogout(request):
    logout(request)
    return redirect('login')

def ordenCompra(request):
    # Crear un objeto HttpResponse con el tipo de contenido de PDF
    response = HttpResponse(content_type='application/pdf')
    # Especificar el nombre del archivo como adjunto
    response['Content-Disposition'] = 'attachment; filename="orden_compra.pdf"'

    # Crear el objeto PDF
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(390, height - 40, "ORDEN DE COMPRA")
    p.drawString(30, height - 40, "Los Pollos Hermanos")

    p.setFont("Helvetica-Bold", 10)
    p.drawString(30, height - 66, "Vendemos de todo menos pollo")
    
    p.setFont("Helvetica", 10)
    p.drawString(30, height - 85, "Dirección: ")
    p.drawString(30, height - 100, "Ciudad, Estado/Provincia, Código Postal: ")
    p.drawString(30, height - 115, "País: ")
    p.drawString(30, height - 130, "Teléfono: ")

    p.setFont("Helvetica", 10)
    p.drawString(30, height - 160, "El siguiente número debe figurar en toda la correspondencia, documentación de envio y")
    p.drawString(30, height - 172, "facturas relacionadas")

    p.drawString(300, height - 85, "4275 Isleta Blvd SW ")
    p.drawString(300, height - 100, "Albuquerque, Nuevo Mexico, 87105")
    p.drawString(300, height - 115, "Estados Unidos")
    p.drawString(300, height - 130, "555-5678")

    p.setFont("Helvetica-Bold", 15)
    p.drawString(30, height - 200, "NÚMERO DE O/C:")

    p.setFont("Helvetica-Bold", 10)
    p.drawString(30, height - 220, "Para: ")
    p.drawString(300, height - 220, "Enviar a: ")

    p.setFont("Helvetica", 10)
    p.drawString(30, height - 235, "Nombre: ")
    p.drawString(30, height - 250, "Compañia: ")
    p.drawString(30, height - 265, "Dirección: ")
    p.drawString(30, height - 280, "Ciudad, Estado/Provincia, Código Postal: ")
    p.drawString(30, height - 295, "Teléfono: ")




    # Tabla de artículos
    data = [
        ['Cantidad', 'Descripción', 'Precio Unitario', 'Total'],
        ['20', 'Descripción 1', '1000', '20000000']
    ]

    table = Table(data, colWidths=[60, 240, 80, 60])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    table.wrapOn(p, width, height)
    table.drawOn(p, 70, height - 370)

    p.setFont("Helvetica", 10)
    p.drawString(400, height - 600, "Subtotal: ")
    p.drawString(400, height - 615, "IVA 19%: ")
    p.drawString(400, height - 630, "Envio: ")
    p.drawString(400, height - 645, "Total: ")

    p.setFont("Helvetica", 10)
    p.drawString(450, height - 600, "Subtotal: ")
    p.drawString(450, height - 615, "IVA 19%: ")
    p.drawString(450, height - 630, "Envio: ")
    p.drawString(450, height - 645, "Total: ")

    # Finalizar el PDF y cerrar el objeto
    p.showPage()
    p.save()

    return response