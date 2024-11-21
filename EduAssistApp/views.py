from Controller.ControllerAsistenteChat import ControllerAsistenteChat
from django.db.models import Max
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg import openapi
from rest_framework.views import APIView

#funcion para autenticar mis credenciales de estudiante
from django.contrib.auth import authenticate
from .models import Perfil

#importaciones para obtener tokens del de la tabla Perfil
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import PerfilTokenObtainPairSerializer, ChatHistorialSerializer
from .models import Perfil, ChatHistorial

class ControllerInter():
    # Hacer que main_engine sea síncrono, llamando async_to_sync dentro de él
    def ResponseAsistenteChat(conversacionEstudiante):
        if conversacionEstudiante:
            try:
                InstanciaControllador= ControllerAsistenteChat()
                mensajeObtenido = async_to_sync(InstanciaControllador.AsistenteChat)(conversacion=conversacionEstudiante)
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


class MetodosValidaciones():
    def isExsistenteEstudiante(self, id_estudiante):
        '''Una funcion para validar si el estudiante existe en la base de datos'''
        estudiante = Perfil.objects.filter(id=id_estudiante)
        if estudiante.exists():
            return Perfil.objects.get(id=id_estudiante)
        else:
            return False

    def isExsistenteConversacion(self, id_conversacion):
        '''Una funcion para validar si la conversacion existe en la base de datos'''
        conversacion = ChatHistorial.objects.filter(id=id_conversacion)
        if conversacion.exists():
            return ChatHistorial.objects.get(id=id_conversacion)
        else:
            return False
class AsistenteEdula(APIView):
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def AsistenteChat(request):
        if request.method == "POST":
            try:
                # Obtener datos del request
                data_requests = request.data
                id_estudiante = data_requests.get("id_estudiante")
                id_conversacion = data_requests.get("id_conversacion")
                mensaje = data_requests.get("mensaje")
                # Validar si el estudiante existe
                estudiante = MetodosValidaciones().isExsistenteEstudiante(id_estudiante)
                if not estudiante:
                    return JsonResponse({"data": 'Estudiante no existe'})


                if not id_conversacion:
                    #crea una nueva conversacion si si id_conversacion es igual a Null en el json de entrada
                    nueva_conversacion_id = ChatHistorial.objects.aggregate(Max('conversation_id'))['conversation_id__max']
                    id_conversacion = (nueva_conversacion_id + 1) if nueva_conversacion_id else 1

                isConversacionExistente = ChatHistorial.objects.filter(conversation_id=id_conversacion).exists()

                #guardar el mensaje del estudiante en la base de datos
                mensajeEstudiante = ChatHistorial.objects.create(
                    estudiante=estudiante,
                    conversation_id=id_conversacion,
                    role='user',
                    content=mensaje
                )

                #obtener el historial de mensajes del estudiante
                historialMensajes = ChatHistorial.objects.filter(conversation_id=id_conversacion)
                #formatear para enviarlo al asistente
                conversacion = [
                    {'role': mensajeEstudiante.role, 'content': mensajeEstudiante.content}
                    for mensajeEstudiante in historialMensajes
                ]
                print(f'conversacion: {conversacion}')
                asistenteIA = ControllerInter.ResponseAsistenteChat(conversacionEstudiante=conversacion)
                '''
                AsistenteEdula = ChatHistorial.objects.create(estudiante=estudiante, conversation_id=id_conversacion, role='assistant', content=asistenteIA)
                return Response({
                    "Estudiante_Mensaje": ChatHistorialSerializer(mensajeEstudiante).data,
                    "Asistente_Edula": ChatHistorialSerializer(AsistenteEdula).data
                })'''
                return JsonResponse({"data": asistenteIA})
            except Exception as e:
                return Response({"Error": f'{str(e)}'})
        else:
            return Response({"error": "Método no disponible"})



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