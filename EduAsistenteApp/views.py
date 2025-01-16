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
    def ResponseAsistenteChat(pregunta, historial):
        if pregunta:
            try:
                InstanciaControllador= ControllerAsistenteChat()
                mensaje_asistente = async_to_sync()(InstanciaControllador.AsistenteChat)(conversacion=pregunta, historial=historial)
                return mensaje_asistente
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

                historial = []

                preguntas_anteriores = PreguntasEstudiante.objects.filter(estudiante=isEstudiante)
                for pregunta_obj in preguntas_anteriores:
                    historial.append({"role": "user", "content": pregunta_obj.preguntas})
                    respuesta_obj = RespuestasAsistenteEdula.objects.filter(preguntas=pregunta_obj).first()
                    if respuesta_obj:
                        historial.append({"role": "assistant", "content": respuesta_obj.respuesta})

                #ahora mandar a llamar la funcion del asistente para que procese la conversacion
                #le peudo mandar solo la pregunta y desde el controlador añadirle el formato
                try:
                    respuesta_Asistente = ControllerInter.ResponseAsistenteChat(pregunta=pregunta, historial=historial)
                    if 'error' in respuesta_Asistente:
                        return Response({"Error": f'{str(e)}'})
                except Exception as e:
                    return Response({"Error": f'{str(e)}'})
                #guardar la la pregunta entrante y la respuesta del asistente
                pregunta_obj = PreguntasEstudiante.objects.create(estudiante=isEstudiante, preguntas=pregunta)
                RespuestasAsistenteEdula.objects.create(estudiante=isEstudiante, preguntas=pregunta_obj, respuesta=respuesta_Asistente.get('Edula_IA'))

                return Response({"data": {
                    "respuesta": respuesta_Asistente,
                    "pregunta": pregunta
                }})
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

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def chat(request):
        if request.method == "POST":
            try:
                data = request.data
                mensaje = data.get('mensaje')
                respuestaEdula = ControllerInter.ResponseAsistenteChat(mensaje)
                print(f'respuesta de vista asistente: {respuestaEdula}')
                return Response({"data": respuestaEdula})
            except Exception as e:
                return Response({"Error": f'{str(e)}'})
        else:
            return Response({"error": "Método no disponible"})

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def limpiarHistorial(request, id=None):
        if request.method == "GET":
            try:
                #mandar el id del estudiante para borrar sus mensajes anteriores
                estudiante = MetodosValidaciones().isExsistenteEstudiante(id)
                if not estudiante:
                    return Response({"data": 'Estudiante no existe'})
                preguntas = PreguntasEstudiante.objects.filter(estudiante=estudiante)
                for pregunta in preguntas:
                    pregunta.delete()
                return Response({"data": "Historial borrado"})
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
