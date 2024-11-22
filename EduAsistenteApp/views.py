from Controller.ControllerAsistenteChat import ControllerAsistenteChat
from asgiref.sync import async_to_sync
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from EduEstudianteApp.models import PerfilEstudiante
from .models import PreguntasEstudiante, RespuestasAsistenteEdula

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
                pregunta = data_requests.get("pregunta")
                if not pregunta:
                    return Response({"data": 'El campo pregunta es requerido'})
                isEstudiante = MetodosValidaciones().isExsistenteEstudiante(id_estudiante)
                if not isEstudiante:
                    return Response({"data": 'Estudiante no existe'})

                historial = [{"role": "system", "content": "Eres un asistente útil."}]

                preguntas_anteriores = PreguntasEstudiante.objects.filter(estudiante=isEstudiante)
                for pregunta_obj in preguntas_anteriores:
                    historial.append({"role": "user", "content": pregunta_obj.preguntas})
                    respuesta_obj = RespuestasAsistenteEdula.objects.filter(preguntas=pregunta_obj).first()
                    if respuesta_obj:
                        historial.append({"role": "assistant", "content": respuesta_obj.respuesta})
                #pregunta actual del estudiante (la entrante del json)
                historial.append({"role": "user", "content": pregunta})
                #ahora mandar a llamar la funcion del asistente para que procese la conversacion
                respuesta_Asistente = 'una respuesta del asistente'

                #guardar la la pregunta entrante y la respuesta del asistente
                pregunta_obj = PreguntasEstudiante.objects.create(estudiante=isEstudiante, preguntas=pregunta)
                RespuestasAsistenteEdula.objects.create(estudiante=isEstudiante, preguntas=pregunta_obj, respuesta=respuesta_Asistente)

                return Response({"data": historial})
            except Exception as e:
                return Response({"Error": f'{str(e)}'})
        else:
            return Response({"error": "Método no disponible"})

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def HistorialEstudiante(request, id=None):
        if request.method == "GET":
            try:
                conversacion  = []
                estudiante = MetodosValidaciones().isExsistenteEstudiante(id)
                if not estudiante:
                    return Response({"data": 'Estudiante no existe'})
                preguntas = PreguntasEstudiante.objects.filter(estudiante=estudiante)
                for pregunta in preguntas:
                    conversacion.append({"role": "user", "content": pregunta.preguntas})
                    respuesta = RespuestasAsistenteEdula.objects.filter(preguntas=pregunta).first()
                    if respuesta:
                        conversacion.append({"role": "assistant", "content": respuesta.respuesta})
                return Response({"data": conversacion})
            except Exception as e:
                return Response({"Error": f'{str(e)}'})
        else:
            return Response({"error": "Método no disponible"})

class MetodosValidaciones():
    def isExsistenteEstudiante(self, id_estudiante):
        try:
            estudiante = PerfilEstudiante.objects.get(id=id_estudiante)
            return estudiante
        except PerfilEstudiante.DoesNotExist:
            return False
