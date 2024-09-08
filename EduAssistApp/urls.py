from django.urls import path
from .views import AsistEdula, LoginEstudiante, PerfilTokenObtainPairView
urlpatterns = [
    path("asistente/chat", AsistEdula.get_response_AV, name="chat av"),
    path('asistenteTest/chat', AsistEdula.responseAsist, name="Chat asistente testing"),
    path('login', LoginEstudiante.login, name='enpoint para el inicio de sesion'),
    path('Crear', LoginEstudiante.createCuenta, name='enpoint para crear cuenta de estudiante'),
    path('Perfil/tokens', PerfilTokenObtainPairView.as_view(), name='endpoint de generacion de tokens para Estudiantes' )
]