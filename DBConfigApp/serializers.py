from rest_framework import serializers
from .models import DocumentosRagGeneral

class DocumentosRagGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentosRagGeneral
        fields = ['id', 'documento']