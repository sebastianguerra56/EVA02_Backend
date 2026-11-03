from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate
from datetime import date

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from .models import Vehiculo

# Create your views here.
def inicio(request):
    return render(request, 'automotoraapp/inicio.html')

def crear_auto(request):
    return render(request, 'automotoraapp/crear.html',{'año_actual': date.today().year, 'fecha_actual': date.today().isoformat()})

def catalogo(request):
    return render(request, 'automotoraapp/catalogo.html')

def ver_auto(request, auto_id):
    return render(request, 'automotoraapp/ver.html')


def editar_auto(request, auto_id):
     auto = Vehiculo.objects.get(id=auto_id)
     if request.method == 'POST':
         auto.marca = request.POST['marca'].lower()
         auto.modelo = request.POST['modelo'].lower()
         auto.año = request.POST['año']
         auto.color = request.POST['color'].lower()
         auto.precio = request.POST['precio']
         auto.kilometraje = request.POST['kilometraje']
         auto.tipo_combustible = request.POST['tipo_combustible'].lower()
         auto.transmision = request.POST['transmision'].lower()
         auto.numero_puertas = request.POST['numero_puertas']
         auto.fecha_registro = request.POST['fecha_registro']

         auto.save()

         return render(request, 'automotoraapp/confirmacion.html', {'auto': auto})
     return render(request, 'automotoraapp/editar.html', {
         'auto': auto
     })

def eliminar_auto(request, auto_id):
    auto = Vehiculo.objects.get(id=auto_id)

    if request.method == 'POST':
        auto.delete()
        return redirect('inicio')

    return render(request, 'automotoraapp/eliminar.html', {
        'auto': auto
    })

def login(request):
    return render(request, 'automotoraapp/login.html')

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            token, creado = Token.objects.get_or_create(user=usuario)
            return Response({
                'mensaje': 'Autenticacion correcta',
                'usuario': usuario.username,
                'token': token.key
            }, status=status.HTTP_200_OK)
        return Response({
            'error': 'Usuario o contraseña incorrectos'             
            }, status=status.HTTP_401_UNAUTHORIZED)

class AutomotoraAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    #Get listar todos los vehículos
    def get(self, request):
        vehiculos = Vehiculo.objects.all()
        datos = []

        for vehiculo in vehiculos:
            datos.append({
                'id': vehiculo.id,
                'marca': vehiculo.marca,
                'modelo': vehiculo.modelo,
                'año': vehiculo.año,
                'color': vehiculo.color,
                'precio': vehiculo.precio,
                'kilometraje': vehiculo.kilometraje,
                'tipo_combustible': vehiculo.tipo_combustible,
                'transmision': vehiculo.transmision,
                'numero_puertas': vehiculo.numero_puertas,
                'fecha_registro': vehiculo.fecha_registro
            })   
        return Response(datos, status=status.HTTP_200_OK)
    
    #Post Registrar un nuevo vehículo
    def post(self, request):

        #Recibir datos del cliente
        marca = request.data.get('marca')
        modelo = request.data.get('modelo')
        año = request.data.get('año')
        color = request.data.get('color')
        precio = request.data.get('precio')
        kilometraje = request.data.get('kilometraje')
        tipo_combustible = request.data.get('tipo_combustible')
        transmision = request.data.get('transmision')
        numero_puertas = request.data.get('numero_puertas')
        fecha_registro = request.data.get('fecha_registro')

        if marca is None or modelo is None or año is None or color is None or precio is None or kilometraje is None or tipo_combustible is None or transmision is None or numero_puertas is None or fecha_registro is None:
            return Response({
                'error': 'Debe proporcionar todos los datos para el vehículo'
            }, status=status.HTTP_400_BAD_REQUEST)

        #Registramos el vehículo en la base de datos
        vehiculo = Vehiculo.objects.create(
            marca=marca.lower(),
            modelo=modelo.lower(),
            año=año,
            color=color.lower(),
            precio=precio,
            kilometraje=kilometraje,
            tipo_combustible=tipo_combustible.lower(),
            transmision=transmision.lower(),
            numero_puertas=numero_puertas,
            fecha_registro=fecha_registro
        )
        return Response({
            'mensaje': 'Vehículo creado correctamente',
            'vehiculo': {
                'id': vehiculo.id,
                'marca': vehiculo.marca,
                'modelo': vehiculo.modelo,
                'año': vehiculo.año,
                'color': vehiculo.color,
                'precio': str(vehiculo.precio),
                'kilometraje': vehiculo.kilometraje,
                'tipo_combustible': vehiculo.tipo_combustible,
                'transmision': vehiculo.transmision,
                'numero_puertas': vehiculo.numero_puertas,
                'fecha_registro': vehiculo.fecha_registro
            }
        }, status=status.HTTP_201_CREATED)

class VehiculoDetalleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    #Get obtener un vehículo por su ID
    def get(self, request, auto_id):
        vehiculo = get_object_or_404(Vehiculo, id=auto_id)
        datos = {
            'id': vehiculo.id,
            'marca': vehiculo.marca,
            'modelo': vehiculo.modelo,
            'año': vehiculo.año,
            'color': vehiculo.color,
            'precio': str(vehiculo.precio),
            'kilometraje': vehiculo.kilometraje,
            'tipo_combustible': vehiculo.tipo_combustible,
            'transmision': vehiculo.transmision,
            'numero_puertas': vehiculo.numero_puertas,
            'fecha_registro': vehiculo.fecha_registro
        }
        return Response(datos, status=status.HTTP_200_OK)
    #DELETE: eliminar un vehículo por su ID
    def delete(self, request, auto_id):
        vehiculo = get_object_or_404(Vehiculo, id=auto_id)

        vehiculo.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    #PUT: actualizar todos los campos editables de un vehículo
    def put(self, request, auto_id):
        vehiculo = get_object_or_404(Vehiculo, id=auto_id)

        # Recibir los datos enviados por el cliente
        marca = request.data.get('marca')
        modelo = request.data.get('modelo')
        año = request.data.get('año')
        color = request.data.get('color')
        precio = request.data.get('precio')
        kilometraje = request.data.get('kilometraje')
        tipo_combustible = request.data.get('tipo_combustible')
        transmision = request.data.get('transmision')
        numero_puertas = request.data.get('numero_puertas')

        # Comprobar que se hayan enviado todos los campos
        if (
            marca is None or
            modelo is None or
            año is None or
            color is None or
            precio is None or
            kilometraje is None or
            tipo_combustible is None or
            transmision is None or
            numero_puertas is None
        ):
            return Response({
                'error': 'Debes enviar todos los datos del vehículo.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Asignar los nuevos datos al vehículo
        vehiculo.marca = marca
        vehiculo.modelo = modelo
        vehiculo.año = año
        vehiculo.color = color
        vehiculo.precio = precio
        vehiculo.kilometraje = kilometraje
        vehiculo.tipo_combustible = tipo_combustible
        vehiculo.transmision = transmision
        vehiculo.numero_puertas = numero_puertas

        # Guardar los cambios en la base de datos
        vehiculo.save()

        return Response({
            'mensaje': 'Vehículo actualizado correctamente',
            'id': vehiculo.id,
            'marca': vehiculo.marca,
            'modelo': vehiculo.modelo,
            'año': vehiculo.año,
            'color': vehiculo.color,
            'precio': str(vehiculo.precio),
            'kilometraje': vehiculo.kilometraje,
            'tipo_combustible': vehiculo.tipo_combustible,
            'transmision': vehiculo.transmision,
            'numero_puertas': vehiculo.numero_puertas,
            'fecha_registro': vehiculo.fecha_registro
        }, status=status.HTTP_200_OK)