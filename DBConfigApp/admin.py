from django.contrib import admin
from .models import DataGeneralChat, DataAsistenteChat, DocumentosRagGeneral, DocumentosRagAsistente

# Register your models here.

admin.site.register(DataGeneralChat)
admin.site.register(DataAsistenteChat)
admin.site.register(DocumentosRagGeneral)
admin.site.register(DocumentosRagAsistente)