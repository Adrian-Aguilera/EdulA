from django.shortcuts import render
from Modules.GeneralModel import *
from Controller.ControllerApp import *
from dotenv import load_dotenv
from asgiref.sync import sync_to_async
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView

class ControllerInter():
    # Hacer que main_engine sea síncrono, llamando async_to_sync dentro de él
    def main_engine(type_engine, message):
        if not type_engine:
            return "Faltan parámetros para inicializar el motor"

        modeAV = type_engine.get("AV", None)

        if modeAV is not None:
            engine = ControllerEduIA(EngineAV=modeAV)
            mensaje = async_to_sync(engine.main_engine)(message)
            return mensaje
        else:
            return "Tipo de motor no definido correctamente"

# Create your views here.
class AsistEdula(APIView):
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id_users': openapi.Schema(type=openapi.TYPE_STRING),
                'type_engine': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'EngineAV': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    },
                    required=['EngineAV']
                ),
                'id_message': openapi.Schema(type=openapi.TYPE_STRING),
                'user_message': openapi.Schema(type=openapi.TYPE_STRING),
                'history_chat': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'system_response': openapi.Schema(type=openapi.TYPE_STRING),
                        'user_response': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                ),
            },
            required=['id_users', 'type_engine', 'id_message', 'user_message']
        )
    )
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def get_response_AV(request):
        if request.method == "POST":
            try:
                data_requests = request.data
                id_users = data_requests.get("id_users")
                type_engine = data_requests.get("type_engine")
                id_message = data_requests.get("id_message")
                user_message = data_requests.get("user_message")
                engine = ControllerInter.main_engine(type_engine, user_message)
                return JsonResponse({"data": engine})
            except Exception as e:
                return Response({"Error": "Fail get data"})
        else:
            return Response({"error": "metodo no disponible"})

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def responseAsist(request):
        if request.method == 'POST':
            try:
                dataRequest = request.data
                type_engine = dataRequest.get("type_engine")
                UserMessage = dataRequest.get('user_message')
                responseMethod = ControllerInter.main_engine(type_engine=type_engine, message=UserMessage)
                return JsonResponse({'data': responseMethod })
            except Exception as e:
                return JsonResponse({'Error Exception': str(e)})
        else:
            return JsonResponse({'Error method': 'metodo no disponible'})