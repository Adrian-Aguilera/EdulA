from django.urls import path
from .views import AsistenteEdula

urlpatterns = [
    path("asistente/chat", AsistenteEdula.AsistenteChat, name="Es el asistente para el estudiante"),
]