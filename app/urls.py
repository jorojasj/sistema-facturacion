from django.urls import path
from . import views
from .views import anular_orden


urlpatterns = [
    path('', views.cargarLogin, name="login"),
    path('logout/', views.cargarLogout, name="logout"),
    path('index/', views.index, name="index"),
    path('agregarOrden/', views.cargarAgregarOrden, name="agregarOrden"),
    path('ordenCompra/', views.ordenCompra, name="ordenCompra"),
    path('ordenCompra/<int:id_orden_compra>/', views.ordenCompra, name='orden_compra'),
    path('editar_orden/<int:id_orden>/', views.editar_orden, name='editar_orden'),
    path('ruta/a/enviar_motivo_rechazo/', views.enviar_motivo_rechazo, name='enviar_motivo_rechazo'),
    path('orden/anular/<int:id_orden>/', anular_orden, name='anular_orden'),
]