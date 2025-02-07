from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("orders/", include("orders.urls")),  # Incluye las URLs de la app orders
    path('admin/', admin.site.urls),
]
