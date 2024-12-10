from Controller.ControllerGeneralChat import GeneralChat
from dotenv import load_dotenv
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

load_dotenv(override=True)

class ControllerInter():
    '''
        Funcion para llamar a la clase GeneralChat
    '''
    def ResponseGeneralChat(message):
        if message:
            try:
                controller= GeneralChat()
                respuesta = async_to_sync(controller.GeneralChat)(message=message)
                return respuesta
            except Exception as e:
                return {"error": f"{str(e)}"}
        else:
            return "Faltan parámetros para inicializar el motor"

class GeneralEdula(APIView):
    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def get_general_chat(request):
        if request.method == "POST":
            try:
                data_requests = request.data
                message = data_requests.get('mesage')
                if message:
                    respuesta = ControllerInter.ResponseGeneralChat(message)
                    return JsonResponse({"data":respuesta})
                else:
                    return Response({"error": "Error engine activate"})

            except Exception as e:
                return Response({"error": f"{str(e)}"})
        else:
            return Response({"error": "metodo no disponible"})

