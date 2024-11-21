from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import PerfilEstudiante

class PerfilTokenObtainPairSerializer(TokenObtainPairSerializer):
    carnet = serializers.CharField(required=True)  # Cambiar el campo a carnet

    def validate(self, attrs):
        # Aquí sobrescribimos la lógica de autenticación para usar el campo carnet
        carnet = attrs.get('carnet')
        password = attrs.get('password')

        if carnet and password:
            estudiante = authenticate(carnet=carnet, password=password)  # Autenticar con carnet y password

            if estudiante is None:
                raise serializers.ValidationError(
                    {'detail': 'No active account found with the given credentials'}
                )
            # Si la autenticación es correcta, generamos el token (esta funcion la hereda del TokenObtainPairSerializer)
            refresh = self.get_token(estudiante)

            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'carnet': estudiante.carnet
            }
        else:
            raise serializers.ValidationError(
                {'detail': 'Must include "carnet" and "password"'}
            )

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilEstudiante
        fields = ['carnet', 'password']

    def create(self, validated_data):
        password = validated_data.get('password')
        instanciaPerfil = PerfilEstudiante(**validated_data)
        #encriptar la contraseña
        instanciaPerfil.set_password(raw_password=password)
        instanciaPerfil.save()
        return instanciaPerfil