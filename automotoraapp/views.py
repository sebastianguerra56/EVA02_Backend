from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Auto
# Create your views here.
def crear_auto(request):
    if request.method == 'POST':
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        descripcion = request.POST.get('descripcion')
        auto = Auto(marca=marca, modelo=modelo, descripcion=descripcion)
        auto.save()
        return redirect('inicio')
    return render(request, 'automotoraapp/crear.html')

def ver_auto(request, auto_id):
    auto = Auto.objects.get(id=auto_id)
    return render(request, 'automotoraapp/detalle.html', {'auto': auto})
