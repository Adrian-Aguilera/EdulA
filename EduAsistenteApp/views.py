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

from .serializers import ChatHistorialSerializer
from .models import Perfil, ChatHistory

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
        conversacion = ChatHistory.objects.filter(id=id_conversacion)
        if conversacion.exists():
            return ChatHistory.objects.get(id=id_conversacion)
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
                    nueva_conversacion_id = ChatHistory.objects.aggregate(Max('conversation_id'))['conversation_id__max']
                    id_conversacion = (nueva_conversacion_id + 1) if nueva_conversacion_id else 1

                isConversacionExistente = ChatHistory.objects.filter(conversation_id=id_conversacion).exists()

                #guardar el mensaje del estudiante en la base de datos
                mensajeEstudiante = ChatHistory.objects.create(
                    estudiante=estudiante,
                    conversation_id=id_conversacion,
                    role='user',
                    content=mensaje
                )

                #obtener el historial de mensajes del estudiante
                historialMensajes = ChatHistory.objects.filter(conversation_id=id_conversacion)
                #formatear para enviarlo al asistente
                conversacion = [
                    {'role': mensajeEstudiante.role, 'content': mensajeEstudiante.content}
                    for mensajeEstudiante in historialMensajes
                ]
                print(f'conversacion: {conversacion}')
                asistenteIA = 'respuesta del asistente'

                AsistenteEdula = ChatHistory.objects.create(estudiante=estudiante, conversation_id=id_conversacion, role='assistant', content=asistenteIA)

                return Response({
                    "Estudiante_Mensaje": ChatHistorialSerializer(mensajeEstudiante).data,
                    "Asistente_Edula": ChatHistorialSerializer(AsistenteEdula).data
                })
            except Exception as e:
                return Response({"Error": f'{str(e)}'})
        else:
            return Response({"error": "Método no disponible"})