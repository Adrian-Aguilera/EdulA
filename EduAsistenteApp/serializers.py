from rest_framework import serializers
from EduEstudianteApp.models import PerfilEstudiante

class PerfilEstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilEstudiante
        fields = ['id', 'carnet']