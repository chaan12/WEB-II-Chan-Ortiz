from django.contrib import admin
from .models import Localidad, Evento, Producto, Boleto

admin.site.register(Localidad)
admin.site.register(Evento)
admin.site.register(Producto)
admin.site.register(Boleto)