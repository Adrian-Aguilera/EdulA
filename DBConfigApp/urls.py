from .views import DataToChromaDB
from django.urls import path

urlpatterns = [
    path("activacion/general", DataToChromaDB.activateGeneralMode, name='activacion de configuracion')
]