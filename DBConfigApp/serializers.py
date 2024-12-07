from rest_framework import serializers
from .models import DocumentosRagGeneral, DocumentosRagAsistente

class DocumentosRagGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentosRagGeneral
        fields = ['id', 'documento', 'referencia_url']

class DocumentosRagAsistenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentosRagAsistente
        fields = ['id', 'documento', 'referencia_url']