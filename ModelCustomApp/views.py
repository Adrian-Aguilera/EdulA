# Create your views here.
from django.shortcuts import render
from Modules.FuncionesIA import *
from Controller.ControllerApp import *
from dotenv import load_dotenv
from asgiref.sync import async_to_sync
import subprocess
from django.http import JsonResponse
#importacion de django-rest.
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
import json
#ollama module
from ollama import Client
from dotenv import load_dotenv
load_dotenv(override=True)
ollamaClient = Client(host=str(os.environ.get("OLLAMACLIENT")))
class CustomModel(APIView):
    #enp para crear un modelCustom
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def createModelCustom(request):
        '''
            Metodo para crear un ModelFile Personalizado
        '''
        if request.method == "POST":
            try:
                dataRequests = request.data['modelfile']
                modelfile = f'''
                    FROM {dataRequests['modelo']}
                    PARAMETER temperature {float(dataRequests['temperatura'])}
                    SYSTEM {dataRequests['systemContent']}
                '''
                modelName = dataRequests['nombre']
                ollamaResponse = callCreateModel(modelName=modelName, modelfile=modelfile)
                return Response(ollamaResponse)
            except Exception as e:
                return Response({'Error': f'{str(e)}'})
        else:
            return Response({'ErrorMethod': 'Metodo no permitido'})

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def showAllModel(request):
        if request.method == 'GET':
            try:
                modelAvailable = ollamaClient.list()  #subprocess.run("ollama list", shell=True)
                return Response({"Models": modelAvailable})
            except Exception as e:
                return Response({"Error": "Error al motrar modelos"})
        else:
            return Response({"Method": "Metodo no disponible"})

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def searchModelCustom(request):
        if request.method == 'POST':
            dataRequest = request.data
            nombreModel = dataRequest['nombre']
            availableModel = ollamaClient.show(nombreModel)
            if availableModel:
                return Response({"Models": availableModel})
            else:
                return Response({"Models": "No se ha encontrado el modelo"})
        else:
            return Response({"Method": "Metodo no disponible"})

    @api_view(['POST'])
    def ConnectOllama(request):
        if request.method == 'POST':
            dataRequest = request.data
            modelo = dataRequest["modelo"]
            role = dataRequest["mensaje"]["role"]
            content = dataRequest["mensaje"]["content"]
            create =  ollamaClient.chat(
                model=modelo,
                messages=[
                {
                    'role': f'{role}',
                    'content': f'{content}',
                },
            ])
            return Response(create)
        else:
            return Response({"Method": "Metodo no disponible"})

    @api_view(['GET'])
    def modelUsed(request):
        if request.method == 'GET':
            try:
                modelUsed = os.environ.get('MODELLM')
                return JsonResponse({'data': modelUsed})
            except Exception as e:
                return JsonResponse({'Exception error': str(e)})
        else:
            return Response({"Method": "Metodo no disponible"})

    @api_view(['POST'])
    def deleteModel(request):
        if request.method == 'POST':
            try:
                data = request.data
                nameModel = data['Model']
                responseRequest = ollama.delete(nameModel)
                return JsonResponse(responseRequest)
            except Exception as e:
                return JsonResponse({'Exception Error': f'error > {str(e)}'})
        else:
            return JsonResponse({'Method': 'Metodo invalido'})

def callCreateModel(modelName,modelfile):
    try:
        ollmaResponse = ollamaClient.create(model=modelName, modelfile=modelfile)
        if ollmaResponse['status'] == "success":
            return {"response": "modelo creado correctamente"}
        else:
            return {"error": "error al crear modelo"}
    except Exception as e:
        return {"FatalError": f"Error al conectar ollma {str(e)}"}