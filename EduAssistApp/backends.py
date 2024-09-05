from django.contrib.auth.backends import BaseBackend
from .models import Perfil

class PerfilBackend(BaseBackend):
    def authenticate(self, request, carnet=None, password=None, **kwargs):
        try:
            perfil = Perfil.objects.get(carnet=carnet)
            if perfil.check_password(password): 
                return perfil  
        except Perfil.DoesNotExist:
            return None 

    def get_user(self, user_id):
        try:
            return Perfil.objects.get(pk=user_id)
        except Perfil.DoesNotExist:
            return None