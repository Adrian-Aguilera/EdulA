from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Perfil

class PerfilTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user): #el campo users en realidad  vine si ya esta autenticado o no, osea el carnet
        print("User>>",user)
        token = super().get_token(user)

        # Aquí puedes agregar campos personalizados al token
        token['carnet'] = user.carnet

        return token