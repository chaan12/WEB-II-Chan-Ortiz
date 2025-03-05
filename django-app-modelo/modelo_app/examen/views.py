from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.utils.timezone import localtime
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Evento, Boleto, Localidad, Producto

def index(request):
    eventos = Evento.objects.all()[:3]
    return render(request, 'examen/index.html', {'eventos': eventos})

def eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'examen/eventos.html', {'eventos': eventos})

def agregar_evento(request):
    localidades = Localidad.objects.filter(estatus=True)
    eventos_hoy = Evento.objects.filter(fecha_inicio__date=timezone.localtime(timezone.now()).date()).order_by('-fecha_inicio')
    return render(request, 'examen/addEvent.html', {'localidades': localidades, 'eventos_hoy': eventos_hoy})

@csrf_exempt

def api_agregar_evento(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nombre = data.get("nombre", "").strip()
            fecha_inicio = data.get("fecha_inicio")
            fecha_fin = data.get("fecha_fin")
            localidad_id = data.get("localidad_id")

            if not nombre or not fecha_inicio or not fecha_fin or not localidad_id:
                return JsonResponse({"success": False, "message": "Todos los campos son obligatorios."}, status=400)

            fecha_inicio = timezone.make_aware(timezone.datetime.fromisoformat(fecha_inicio))
            fecha_fin = timezone.make_aware(timezone.datetime.fromisoformat(fecha_fin))
            localidad = get_object_or_404(Localidad, id=localidad_id)

            if fecha_inicio < timezone.now():
                return JsonResponse({"success": False, "message": "La fecha de inicio debe ser mayor o igual a hoy."}, status=400)

            if fecha_fin <= fecha_inicio:
                return JsonResponse({"success": False, "message": "La fecha final debe ser mayor que la fecha de inicio."}, status=400)

            evento = Evento.objects.create(name=nombre, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, localidad=localidad)
            return JsonResponse({"success": True, "message": "Evento agregado correctamente.", "evento_id": evento.id}, status=201)

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Método no permitido."}, status=405)

def eventos_hoy(request):
    hoy = timezone.now().date()
    eventos = Evento.objects.filter(created_at__date=hoy).order_by('-created_at')
    eventos_data = [{
        "id": evento.id,
        "name": evento.name,
        "fecha_inicio": evento.fecha_inicio.strftime("%Y-%m-%d %H:%M"),
        "fecha_fin": evento.fecha_fin.strftime("%Y-%m-%d %H:%M"),
        "localidad": evento.localidad.name
    } for evento in eventos]
    return JsonResponse({"eventos": eventos_data})

@csrf_exempt
def eliminar_evento(request, evento_id):
    if request.method == "DELETE":
        try:
            evento = Evento.objects.get(id=evento_id)
            evento.delete()
            return JsonResponse({"success": True, "message": "Evento eliminado correctamente."})
        except Evento.DoesNotExist:
            return JsonResponse({"success": False, "message": "El evento no existe."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    
    return JsonResponse({"success": False, "message": "Método no permitido."}, status=405)

def boletos(request, evento_id=None):
    evento = get_object_or_404(Evento, id=evento_id) if evento_id else None
    boletos = Boleto.objects.filter(evento=evento) if evento else Boleto.objects.all()
    return render(request, 'examen/boletos.html', {'boletos': boletos, 'evento': evento})

def detalle_boleto(request, boleto_id):
    boleto = get_object_or_404(Boleto, id=boleto_id)
    return render(request, 'examen/boletoID.html', {'boleto': boleto})

def boletos_por_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    boletos = Boleto.objects.filter(evento=evento)
    sin_boletos = not boletos.exists()
    return render(request, 'examen/boletos.html', {'boletos': boletos, 'evento': evento, 'sin_boletos': sin_boletos})

def agregar_boleto(request):
    return render(request, 'examen/addBoleto.html')

def productos(request):
    productos = Producto.objects.all()
    return render(request, 'examen/productos.html', {'productos': productos})

def agregar_producto(request):
    localidades = Localidad.objects.all()  
    return render(request, 'examen/addProduct.html', {'localidades': localidades})

def productos_hoy(request):
    hoy = timezone.localtime(timezone.now()).date()
    productos = Producto.objects.filter(created_at__date=hoy).order_by('-id')
    productos_data = [{
        "id": producto.id,
        "name": producto.name,
        "precio": producto.precio,
        "localidad": producto.localidad.name if producto.localidad else "Sin localidad"
    } for producto in productos]
    return JsonResponse({"productos": productos_data})

@csrf_exempt

def api_agregar_producto(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nombre = data.get("nombre")
            precio = data.get("precio")
            localidad_id = data.get("localidad_id")

            if not nombre or not precio or not localidad_id:
                return JsonResponse({"success": False, "message": "Todos los campos son obligatorios."}, status=400)

            if float(precio) <= 0:
                return JsonResponse({"success": False, "message": "El precio debe ser mayor a 0."}, status=400)

            hoy = timezone.localtime(timezone.now()).date()

            productos_hoy = Producto.objects.filter(id__gte=1).count()
            if productos_hoy >= 10:
                return JsonResponse({"success": False, "message": "No puedes agregar más de 10 productos por día."}, status=400)

            localidad = Localidad.objects.get(id=localidad_id)
            nuevo_producto = Producto.objects.create(name=nombre, precio=precio, localidad=localidad)

            return JsonResponse({"success": True, "message": "Producto agregado correctamente.", "producto_id": nuevo_producto.id}, status=201)

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Método no permitido."}, status=405)

@csrf_exempt
def api_eliminar_producto(request, producto_id):
    if request.method == "DELETE":
        try:
            producto = Producto.objects.get(id=producto_id)
            producto.delete()
            return JsonResponse({"success": True, "message": "Producto eliminado correctamente."}, status=200)
        except Producto.DoesNotExist:
            return JsonResponse({"success": False, "message": "Producto no encontrado."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Método no permitido."}, status=405)