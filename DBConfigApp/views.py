from Modules.FuncionesIA import *
from Controller.DBController import ControllerDataBase
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from EduGeneralApp.models import General_Collection
from EduAsistenteApp.models import AssistantCollection
from .models import DocumentosRagGeneral, DocumentosRagAsistente
from .serializers import DocumentosRagGeneralSerializer, DocumentosRagAsistenteSerializer

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
                controller = ControllerDataBase()
                documentos = DocumentosRagGeneral.objects.all()
                DocumentosSerializer = DocumentosRagGeneralSerializer(documentos, many=True)
                nombre_coleccion  = General_Collection.objects.all().first().Nombre_Coleccion
                crear_coleccion = controller.createCollection(
                    documentos=DocumentosSerializer.data,
                    nombre_Coleccion=nombre_coleccion
                )
                if crear_coleccion.get('success'):
                    return Response({"success": "Coleccion Embedding creada Exitosamente"})
                else:
                    return Response({"error": crear_coleccion.get('error')})
            except Exception as e:
                return Response({"Error": f"{str(e)}"})
        else:
            return Response({"error": "metodo no disponible"})

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def activateAsistentMode(request):
        if request.method == "GET":
            try:
                controller = ControllerDataBase()
                documentos = DocumentosRagAsistente.objects.all()
                DocumentosSerializer = DocumentosRagAsistenteSerializer(documentos, many=True)
                nombre_coleccion  = AssistantCollection.objects.all().first().Nombre_Coleccion
                crear_coleccion = controller.createCollection(
                    documentos=DocumentosSerializer.data,
                    nombre_Coleccion=nombre_coleccion
                )
                if crear_coleccion.get('success'):
                    return Response({"success": "Coleccion Embedding creada Exitosamente"})
                else:
                    return Response({"error": crear_coleccion.get('error')})
            except Exception as e:
                return Response({"Error": f"{str(e)}"})
        else:
            return Response({"error": "metodo no disponible"})

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def showDocuments(request):
        if request.method == "GET":
            try:
                documentos_General = DocumentosRagGeneral.objects.all()
                documentos_Asistente = DocumentosRagAsistente.objects.all()
                DocumentosGeneralSerializer = DocumentosRagGeneralSerializer(documentos_General, many=True)
                DocumentosAsistenteSerializer = DocumentosRagAsistenteSerializer(documentos_Asistente, many=True)
                return Response({"success": {
                    "documentos General": DocumentosGeneralSerializer.data,
                    "documentos Asistente": DocumentosAsistenteSerializer.data
                }})
            except Exception as e:
                return Response({"Error": f"{str(e)}"})
        else:
            return Response({"error": "metodo no disponible"})