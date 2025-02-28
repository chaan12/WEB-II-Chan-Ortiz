from django.shortcuts import render
from .models import Evento, Boleto

def index(request):
    eventos = Evento.objects.all()[:3]
    return render(request, 'examen/index.html', {'eventos': eventos})

def boletos(request):
    boletos = Boleto.objects.all()
    return render(request, 'examen/boletos.html', {'boletos': boletos})

def eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'examen/eventos.html', {'eventos': eventos})