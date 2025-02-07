from django.urls import path
from . import views  # Importamos views.py

urlpatterns = [
    path("list", views.indexOrders, name="order-list"),
]
