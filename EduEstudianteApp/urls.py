from django.urls import path
from .views import LoginEstudiante, PerfilTokenObtainPairView

urlpatterns = [
    path('login', LoginEstudiante.login, name='Inicio de sesion'),
    path('Crear', LoginEstudiante.createCuenta, name='crear cuenta de estudiante'),
    path('Perfil/tokens', PerfilTokenObtainPairView.as_view(), name='endpoint de generacion de tokens para Estudiantes' )
]