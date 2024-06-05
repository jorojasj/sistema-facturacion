from io import BytesIO
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *

#IMPORTS DEL PDF
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# Create your views here.
def index(request):
    ordenes = OrdenCompra.objects.all()
    return render(request,"index.html", {'ordenes':ordenes})

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


def cargarAgregarOrden(request):
    if request.method == 'POST':
        form = OrdenCompraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = OrdenCompraForm()
    return render(request, 'agregarOrden.html', {'form': form})

def ordenCompra(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="orden_compra.pdf"'

    orden = OrdenCompra.objects.all()

    buffer = BytesIO()

    # Crear el objeto PDF
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    for orden in orden:
        # Título
        p.setFont("Helvetica-Bold", 16)
        p.drawString(390, height - 40, "ORDEN DE COMPRA")
        p.drawString(30, height - 40, "Los Pollos Hermanos")

        p.setFont("Helvetica-Bold", 10)
        p.drawString(30, height - 66, "Vendemos de todo menos pollo")
        
        p.setFont("Helvetica", 10)
        p.drawString(30, height - 130, "Teléfono: ")

        p.setFont("Helvetica", 10)
        p.drawString(30, height - 160, "El siguiente número debe figurar en toda la correspondencia, documentación de envio y")
        p.drawString(30, height - 172, "facturas relacionadas")

        p.drawString(30, height - 85, "4275 Isleta Blvd SW ")
        p.drawString(30, height - 100, "Albuquerque, Nuevo Mexico, 87105")
        p.drawString(30, height - 115, "Estados Unidos")
        p.drawString(76, height - 130, "555-5678")

    

        p.setFont("Helvetica-Bold", 15)
        p.drawString(30, height - 200, f"NÚMERO DE O/C: {orden.numero_compra}")

        p.setFont("Helvetica-Bold", 10)
        p.drawString(30, height - 220, "Para: ")
        p.drawString(300, height - 220, "Enviar a: ")

        p.setFont("Helvetica", 10)
        p.drawString(30, height - 235, "Nombre:")
        p.drawString(30, height - 250, "Compañia:")
        p.drawString(30, height - 265, "Dirección: ")
        p.drawString(30, height - 280, "Ciudad, Estado/Provincia, Código Postal: ")
        p.drawString(30, height - 295, "Teléfono: ")

        p.setFont("Helvetica", 10)
        p.drawString(300, height - 235, f"{orden.nombre_cliente}")
        p.drawString(300, height - 250, f"{orden.compania}")
        p.drawString(300, height - 265, f"{orden.direccion}")
        p.drawString(300, height - 280, f"{orden.ciudad}, {orden.estado_provincia}, {orden.postal}")
        p.drawString(300, height - 295, f"{orden.telefono}")

        total1 = orden.cantidad * orden.precio_producto

        data = [
            ['Cantidad', 'Descripción', 'Precio Unitario', 'Total'],
            [f'{orden.cantidad}', f'{orden.nombre_producto}', f'${orden.precio_producto}', f"${total1}"]
        ]

        table = Table(data, colWidths=[60, 240, 80, 60])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        table.wrapOn(p, width, height)
        table.drawOn(p, 70, height - 370)

        subtotal = total1
        iva = subtotal * 0.19
        envio = 5000
        total = subtotal + iva + envio

        p.setFont("Helvetica", 10)
        p.drawString(400, height - 600, "Subtotal: ")
        p.drawString(400, height - 615, "IVA 19%: ")
        p.drawString(400, height - 630, "Envio: ")
        p.drawString(400, height - 645, "Total: ")

        p.setFont("Helvetica", 10)
        p.drawString(450, height - 600, f"${subtotal}")
        p.drawString(450, height - 615, f"${iva:.0f}")
        p.drawString(450, height - 630, f"${envio}")
        p.drawString(450, height - 645, f"${total:.0f}")
        
        p.showPage()

    # Finalizar el PDF y cerrar el objeto
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response