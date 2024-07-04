from django.urls import path
from . import views

urlpatterns = [
    path('', views.cargarLogin, name="login"),
    path('logout/', views.cargarLogout, name="logout"),
    path('index/', views.index, name="index"),
    path('agregarOrden/', views.cargarAgregarOrden, name="agregarOrden"),
    path('ordenCompra/', views.ordenCompra, name="ordenCompra"),
    path('ordenCompra/<int:id_orden_compra>/', views.ordenCompra, name='orden_compra'),
    path('editar_orden/<int:id_orden>/', views.editar_orden, name='editar_orden'),
]