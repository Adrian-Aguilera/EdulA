from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import PerfilTokenObtainPairSerializer, PerfilSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class PerfilTokenObtainPairView(TokenObtainPairView):
    serializer_class = PerfilTokenObtainPairSerializer


class LoginEstudiante(APIView):
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def login(request):
        if request.method == 'POST':
            try:
                data = request.data
                carnet = data.get('carnet')
                password = data.get('password')
                serializerTokens = PerfilTokenObtainPairSerializer()
                obtenerTokens = serializerTokens.validate(attrs={'carnet': carnet, 'password': password})
                return Response(obtenerTokens)
            except Exception as e:
                return Response({"Error Exception": f"{str(e)}"})
        else:
            return Response({"Error Method": "metodo no permitido"})

    @api_view(['POST'])
    def createCuenta(request):
        if request.method == 'POST':
            try:
                data = request.data
                serializerPerfil = PerfilSerializer(data=data)
                if serializerPerfil.is_valid():
                    serializerPerfil.save()
                    return Response({"datos": serializerPerfil.data})
                else:
                    return Response({"Error": serializerPerfil.errors, 'mensaje': 'No se pudo registrar el estudiante'})
            except Exception as e:
                return Response({"Error Exception": f"{str(e)}"})
        else:
            return Response({"Error Method": "metodo no permitido"})