from django.urls import path
from .views import AsistEdula
urlpatterns = [
    path("asistente/chat", AsistEdula.get_response_AV, name="chat av"),
    path('asistenteTest/chat', AsistEdula.responseAsist, name="Chat asistente testing")
]