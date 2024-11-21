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
                return Response({"data": 'Estudiante no existe'})
            except Exception as e:
                return Response({"Error": f'{str(e)}'})
        else:
            return Response({"error": "Método no disponible"})