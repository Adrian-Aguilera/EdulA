from django.urls import path
from .views import AsistenteEdula, LoginEstudiante, PerfilTokenObtainPairView
urlpatterns = [
    path("asistente/chat", AsistenteEdula.AsistenteChat, name="Es el asistente para el estudiante"),
    path('login', LoginEstudiante.login, name='enpoint para el inicio de sesion'),
    path('Crear', LoginEstudiante.createCuenta, name='enpoint para crear cuenta de estudiante'),
    path('Perfil/tokens', PerfilTokenObtainPairView.as_view(), name='endpoint de generacion de tokens para Estudiantes' )
]