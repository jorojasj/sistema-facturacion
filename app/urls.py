from django.urls import path
from . import views

urlpatterns = [
    path('', views.cargarLogin, name="login"),
    path('logout/', views.cargarLogout, name="logout"),
    path('index/', views.index, name="index"),
    path('agregarOrden/', views.cargarAgregarOrden, name="agregarOrden"),
    path('ordenCompra/', views.ordenCompra, name="ordenCompra"),
]