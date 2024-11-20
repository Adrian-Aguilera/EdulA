from Controller.ControllerAsistenteChat import ControllerAsistenteChat
from dotenv import load_dotenv
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView

#funcion para autenticar mis credenciales de estudiante
from django.contrib.auth import authenticate
from .models import Perfil

#importaciones para obtener tokens del de la tabla Perfil
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import PerfilTokenObtainPairSerializer

class ControllerInter():
    # Hacer que main_engine sea síncrono, llamando async_to_sync dentro de él
    def ResponseAsistenteChat(message):
        if message:
            try:
                InstanciaControllador= ControllerAsistenteChat()
                mensajeObtenido = async_to_sync(InstanciaControllador.AsistenteChat)(message)
                return mensajeObtenido
            except Exception as e:
                return {"error": f"{str(e)}"}
        else:
            return "Faltan parámetros para inicializar el chat del asistente"

    def insertarDatos(carnet, password):
        if not carnet or not password:
            return {"informacion": "El carnet y la contraseña son obligatorios."}
        try:
            if Perfil.objects.filter(carnet=carnet).exists():
                return {"informacion": "Ya existe un estudiante con este carnet."}
            nuevoEstudiante = Perfil(carnet=carnet)
            nuevoEstudiante.set_password(raw_password=password)
            nuevoEstudiante.save()

            return {"informacion": f'El estudiante con carnet {nuevoEstudiante.carnet} se ha registrado exitosamente.'}

        except Exception as e:
            return {"informacion": f'No se pudo registrar el estudiante. Error: {str(e)}'}
        #return({"informacion": f'{nuevoEstudiante.carnet} se ha registrado'})

# Create your views here.
class AsistenteEdula(APIView):
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def AsistenteChat(request):
        if request.method == "POST":
            try:
                data_requests = request.data
                id_users = data_requests.get("id_users")
                id_message = data_requests.get("id_message")
                mensaje = data_requests.get("mensaje")
                print(f'id_users: {id_users} \n id_message: {id_message} \n user_message: {mensaje}')
                engine = ControllerInter.ResponseAsistenteChat(message=mensaje)
                return JsonResponse({"data": engine})
            except Exception as e:
                return Response({"Error": "Fail get data"})
        else:
            return Response({"error": "metodo no disponible"})


class LoginEstudiante(APIView):
    @api_view(['POST'])
    def login(request):
        if request.method == 'POST':
            try:
                data = request.data
                carnet = data.get('carnet')
                password = data.get('password')
                serializerTokens = PerfilTokenObtainPairSerializer()
                obtenerTokens = serializerTokens.validate(attrs={'carnet': carnet, 'password': password})
                return JsonResponse(obtenerTokens)
            except Exception as e:
                return JsonResponse({"Error Exception": f"{str(e)}"})
        else:
            return JsonResponse({"Error Method": "metodo no permitido"})

    @api_view(['POST'])
    def createCuenta(request):
        if request.method == 'POST':
            try:
                data = request.data
                carnet = data.get('carnet')
                password = data.get('pass')
                insertarDatos = ControllerInter.insertarDatos(carnet=carnet, password=password)
                return JsonResponse({"datos": insertarDatos})
            except Exception as e:
                return JsonResponse({"Error Exception": f"{str(e)}"})
        else:
            return JsonResponse({"Error Method": "metodo no permitido"})


class PerfilTokenObtainPairView(TokenObtainPairView):
    serializer_class = PerfilTokenObtainPairSerializer