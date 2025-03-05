from django.urls import path
from . import views

urlpatterns = [
    # Página Principal
    path('index/', views.index, name='index'),

    # Eventos
    path('eventos/', views.eventos, name='eventos'),
    path('agregar-evento/', views.agregar_evento, name='agregar_evento'),
    path('api/agregar-evento/', views.api_agregar_evento, name='api_agregar_evento'),
    path('api/eventos-hoy/', views.eventos_hoy, name='eventos_hoy'),
    path('api/eliminar-evento/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),

    # Boletos
    path('boletos/', views.boletos, name='boletos'),
    path('boletos/<int:boleto_id>/', views.detalle_boleto, name='detalle_boleto'),
    path('boletos/evento/<int:evento_id>/', views.boletos_por_evento, name='boletos_por_evento'),
    path('agregar-boleto/', views.agregar_boleto, name='agregar_boleto'),

    # Productos
    path('productos/', views.productos, name='productos'),
    path('agregar-producto/', views.agregar_producto, name='agregar_producto'),
    path('api/agregar-producto/', views.api_agregar_producto, name='api_agregar_producto'),
    path('api/productos-hoy/', views.productos_hoy, name='productos_hoy'),
    path('api/eliminar-producto/<int:producto_id>/', views.api_eliminar_producto, name='api_eliminar_producto'),
]