from django.db import models

class Localidad(models.Model):
    name = models.CharField(max_length=100, null=False)
    estatus = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Evento(models.Model):
    name = models.CharField(max_length=300, null=False)
    fecha_inicio = models.DateTimeField(null=False)
    fecha_fin = models.DateTimeField(null=False)
    localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE)
    imagen_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Producto(models.Model):
    name = models.CharField(max_length=200)
    precio = models.FloatField()
    localidad = models.ForeignKey(Localidad, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.name

class Boleto(models.Model):
    precio = models.FloatField(null=False)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fecha = models.DateTimeField(null=True, blank=True)
    imagen_url = models.URLField(null=True, blank=True)  

    def __str__(self):
        return f"Boleto para {self.evento.name} - ${self.precio}"