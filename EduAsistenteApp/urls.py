from django.urls import path
from .views import AsistenteEdula

urlpatterns = [
    path("asistente/chat", AsistenteEdula.AsistenteChat, name="Es el asistente para el estudiante"),
    path("asistente/historial/<int:id>", AsistenteEdula.HistorialEstudiante, name="Historial de conversacion del estudiante"),
    path("asistente/chat/test", AsistenteEdula.chat, name="Conversacion directa con el asistente"),
    path("asistente/historial/limpiar/<int:id>", AsistenteEdula.limpiarHistorial, name="Limpiar historial del estudiante"),
]