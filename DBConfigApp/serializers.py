from rest_framework import serializers
from .models import DocumentosRagGeneral, DocumentosRagAsistente

class DocumentosRagGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentosRagGeneral
        fields = ['id', 'documento']

class DocumentosRagAsistenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentosRagAsistente
        fields = ['id', 'documento']