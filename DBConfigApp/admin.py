from django.contrib import admin
from .models import DataGeneralChat, DataAsistenteChat, DocumentosRagGeneral

# Register your models here.

admin.site.register(DataGeneralChat)
admin.site.register(DataAsistenteChat)
admin.site.register(DocumentosRagGeneral)