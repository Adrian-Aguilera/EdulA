from Modules.GeneralModel import *
from Controller.ControllerApp import *
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import DataGeneralChat, DataAsistenteChat
from EduGeneralApp.models import NameCollectionGeneral
from EduAssistApp.models import AssistantCollection
#clase que se encargara de gestionar la parte de la informacion de los modelos
class DataToChromaDB(APIView):
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def activateGeneralMode(request):
        if request.method == "GET":
            try:
                dbController = ControllerDataBase()
                configInstance = NameCollectionGeneral.objects.all()
                getNameCollection = configInstance[0].nameCollection
                getDataContent = DataGeneralChat.objects.all()[0].dataContent
                print(f'data: {getNameCollection}')
                response = dbController.createDatabase(nameCollection=getNameCollection, dataContent=getDataContent)
                return JsonResponse(response)
            except Exception as e:
                return Response({"Error": f"{str(e)}"})
        else:
            return Response({"error": "metodo no disponible"})

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def activateAsistentMode(request):
        if request.method == "GET":
            try:
                dbController = ControllerDataBase()
                configInstance = AssistantCollection.objects.all()
                getNameCollection = configInstance[0].nameCollection
                getDataContent = DataAsistenteChat.objects.all()[0].dataContent
                print(f'name Collection: {getNameCollection} \n')
                print(f'data: {getDataContent} \n')
                response = dbController.createDatabase(nameCollection=getNameCollection, dataContent=getDataContent)
                return JsonResponse(response)
            except Exception as e:
                return Response({"Error": f"{str(e)}"})
        else:
            return Response({"error": "metodo no disponible"})