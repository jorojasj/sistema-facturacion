from io import BytesIO
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
from .forms import OrdenCompraForm
from .models import OrdenCompra 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

#IMPORTS DEL PDF
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io
from io import BytesIO
from reportlab.lib.pagesizes import letter


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

def obtener_siguiente_numero_compra():
    ultima_orden = OrdenCompra.objects.all().order_by('numero_compra').last()
    if ultima_orden:
        return ultima_orden.numero_compra + 1
    return 1


def exportar_pdf(request, orden_id):
    # Obtener la orden de compra específica por ID
    orden = get_object_or_404(OrdenCompra, id=orden_id)

    # Configurar la respuesta HTTP para el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="orden_{}.pdf"'.format(orden_id)

    # Crear un objeto PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # Aquí agregarías el código para dibujar en el PDF usando los datos de 'orden'
    # Por ejemplo:
    p.drawString(100, 800, "ID de la Orden: {}".format(orden.id))
    p.drawString(100, 780, "Detalles de la Orden: {}".format(orden.detalles))

    # Finalizar el PDF
    p.showPage()
    p.save()

    # Mover al inicio del buffer y devolver la respuesta
    buffer.seek(0)
    return response

def mi_vista(request):
    if request.method == 'POST':
        form = MotivoRechazoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Asegúrate de que esta línea esté correctamente indentada
    else:
        form = MotivoRechazoForm()
    
    return render(request, 'tu_template_rechazo.html', {'form': form})


@csrf_exempt
def enviar_motivo_rechazo(request):
    if request.method == 'POST':
        # Aquí procesas la solicitud
        try:
            # Lógica para procesar el motivo del rechazo
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)



def rechazar_entrega(request, entrega_id):
    entrega = Entrega.objects.get(id=entrega_id)
    if request.method == 'POST':
        form = MotivoRechazoForm(request.POST)
        if form.is_valid():
            motivo_rechazo = form.save(commit=False)
            motivo_rechazo.entrega = entrega
            motivo_rechazo.save()
            # Redirige o maneja la lógica después del rechazo
            return redirect('alguna_vista')
        else:
            print(form.errors)  # Imprime los errores del formulario en la consola
    else:
        form = MotivoRechazoForm()
    return render(request, 'tu_template.html', {'form': form})


def anular_orden(request, id_orden):
    orden = get_object_or_404(OrdenCompra, numero_compra=id_orden)
    orden.estado = 'nula'  # Asegúrate de que 'nula' sea un estado válido en tu modelo
    orden.save()
    # Redirige al usuario de vuelta a la página de donde vino o a cualquier otra página
    return redirect('index')




def descargar_factura(request, id_orden_compra):
    # Obtener la orden de compra específica por ID
    orden_compra = get_object_or_404(OrdenCompra, id=id_orden_compra)
    
    # Determinar si la orden está anulada
    es_anulada = orden_compra.estado == 'nula'
    
    # Preparar los datos para el PDF
    datos_para_pdf = {
        'id_orden_compra': id_orden_compra,
        'es_anulada': es_anulada,  # Agregar el estado de anulación
        # Agregar más datos si es necesario
    }
    
    # Generar el PDF
    pdf = generate_pdf('plantilla_factura.html', datos_para_pdf)
    
    # Crear la respuesta HTTP con el PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{id_orden_compra}.pdf"'
    
    return response


def editar_orden(request, id_orden):
    orden = get_object_or_404(OrdenCompra, pk=id_orden)
    if request.method == 'POST':
        form = OrdenCompraForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            orden.estado = 'rectificada'  # Cambia el estado a rectificada
            orden.save()
            return redirect('index')  # Redirige al índice
    else:
        form = OrdenCompraForm(instance=orden)
    return render(request, 'editar_orden.html', {'form': form})


def ordenCompra(request, id_orden_compra):
    # Obtener la orden de compra específica por ID
    orden_compra = get_object_or_404(OrdenCompra, numero_compra=id_orden_compra)

    # Preparar la respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="orden_compra_{id_orden_compra}.pdf"'

    # Crear un buffer para el PDF
    buffer = BytesIO()

    # Crear el objeto PDF, usando el buffer como su "archivo"
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Generar el PDF usando los datos de `orden_compra`
    p.setFont("Helvetica-Bold", 16)
    p.drawString(390, height - 40, "ORDEN DE COMPRA")
    p.drawString(30, height - 40, "Los Pollos Hermanos")
    p.setFont("Helvetica-Bold", 10)
    p.drawString(30, height - 66, "Vendemos de todo menos pollo")
    p.setFont("Helvetica", 10)
    p.drawString(30, height - 85, "4275 Isleta Blvd SW ")
    p.drawString(30, height - 100, "Albuquerque, Nuevo Mexico, 87105")
    p.drawString(30, height - 115, "Chile")
    p.drawString(76, height - 130, "+56 9 8166 7610")

    # Información de la orden de compra
    p.setFont("Helvetica-Bold", 15)
    p.drawString(30, height - 200, f"NÚMERO DE O/C: {orden_compra.numero_compra}")

    p.setFont("Helvetica-Bold", 10)
    p.drawString(30, height - 220, "Para: ")
    p.drawString(300, height - 220, "Enviar a: ")

    p.setFont("Helvetica", 10)
    p.drawString(30, height - 235, "Nombre:")
    p.drawString(30, height - 250, "Compañia:")
    p.drawString(30, height - 265, "Dirección: ")
    p.drawString(30, height - 280, "Ciudad, Estado/Provincia, Código Postal: ")
    p.drawString(30, height - 295, "Teléfono: ")

    p.drawString(300, height - 235, f"{orden_compra.nombre_cliente}")
    p.drawString(300, height - 250, f"{orden_compra.compania}")
    p.drawString(300, height - 265, f"{orden_compra.direccion}")
    p.drawString(300, height - 280, f"{orden_compra.ciudad}, {orden_compra.estado_provincia}, {orden_compra.postal}")
    p.drawString(300, height - 295, f"{orden_compra.telefono}")
    # Calcula el total o usa un campo si ya existe
    total = orden_compra.cantidad * orden_compra.precio_producto
    p.drawString(100, 720, f"Total: ${total}")

    # Continuación del código existente...

    data = [
        ['Cantidad', 'Descripción', 'Precio Unitario', 'Total'],
        [f'{orden_compra.cantidad}', f'{orden_compra.nombre_producto}', f'${orden_compra.precio_producto}', f"${total}"]
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

    # Asumiendo que 'total1' es el subtotal calculado previamente, si no, necesitas calcularlo
    subtotal = total  # Si 'total' es el subtotal de todos los productos
    iva = subtotal * 0.19
    envio = 5000
    total_final = subtotal + iva + envio  # Cambiado a 'total_final' para evitar confusión con el 'total' anterior

    p.setFont("Helvetica", 10)
    p.drawString(400, height - 600, "Subtotal: ")
    p.drawString(400, height - 615, "IVA 19%: ")
    p.drawString(400, height - 630, "Envio: ")
    p.drawString(400, height - 645, "Total: ")

    p.setFont("Helvetica", 10)
    p.drawString(450, height - 600, f"${subtotal}")
    p.drawString(450, height - 615, f"${iva:.0f}")
    p.drawString(450, height - 630, f"${envio}")
    p.drawString(450, height - 645, f"${total_final:.0f}")

    # Finalizar el PDF
    p.showPage()
    p.save()

    # Mover el puntero al inicio del buffer y escribir el PDF en la respuesta HTTP
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response

