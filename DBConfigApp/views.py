from Modules.FuncionesIA import *
from Controller.DBController import ControllerDataBase
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import DataGeneralChat, DataAsistenteChat
from EduGeneralApp.models import General_Collection
from EduAssistApp.models import AssistantCollection

'''
Esta es una Vista que se encarga de crear la base de datos
'''
class DataToChromaDB(APIView):
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def activateGeneralMode(request):
        '''
            Esta es un enpoint que permite crear una coleccion con la informacion de la base de datos principal
            para hacerlo embeding y que lo use la base de datos de Chroma (BD de vectorial)

            pd: primero se tiene que crear una coleccion en la base de datos principal, y esta tiene que tener informacion asociada en la tabla DataGeneralChat (se puede agregar data desde el admin de la app)
        '''
        if request.method == "GET":
            try:
                dbController = ControllerDataBase()
                configInstance = General_Collection.objects.all()
                getNameCollection = configInstance[0].Nombre_Coleccion
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
                getNameCollection = configInstance[0].Nombre_Coleccion
                getDataContent = DataAsistenteChat.objects.all()[0].dataContent
                print(f'name Collection para Asistente: {getNameCollection} \n')
                print(f'data de Asistente: {getDataContent} \n')
                response = dbController.createDatabase(nameCollection=getNameCollection, dataContent=getDataContent)
                return JsonResponse(response)
            except Exception as e:
                return Response({"Error": f"{str(e)}"})
        else:
            return Response({"error": "metodo no disponible"})