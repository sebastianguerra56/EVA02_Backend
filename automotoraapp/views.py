from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Auto

# Create your views here.
def inicio(request):
    return render(request, 'automotoraapp/inicio.html')

def crear_auto(request):
    if request.method == 'POST':
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        año = request.POST.get('año')
        color = request.POST.get('color')
        precio = request.POST.get('precio')
        kilometraje = request.POST.get('kilometraje')
        tipo_combustible = request.POST.get('tipo_combustible')
        transmision = request.POST.get('transmision')
        numero_puertas = request.POST.get('numero_puertas')
        fecha_registro = request.POST.get('fecha_registro')

        auto = Auto(marca=marca.lower(), modelo=modelo.lower(), año=año, color=color.lower(), precio=precio, kilometraje=kilometraje, tipo_combustible=tipo_combustible, transmision=transmision, numero_puertas=numero_puertas, fecha_registro=fecha_registro)
        auto.save()
        return render(request, 'automotoraapp/confirmacion.html', {'auto': auto})
    return render(request, 'automotoraapp/crear.html')

def catalogo(request):
    autos = Auto.objects.all()
    return render(request, 'automotoraapp/catalogo.html', {'autos': autos})

def ver_auto(request, auto_id):
    auto = Auto.objects.get(id=auto_id)
    return render(request, 'automotoraapp/ver.html', {'auto': auto})
