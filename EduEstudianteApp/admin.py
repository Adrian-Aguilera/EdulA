from django.contrib import admin
from .models import PerfilEstudiante
# Register your models here.

class PerfilEstudianteAdmin(admin.ModelAdmin):
    list_display = ('id','carnet')
    search_fields  = ('id','carnet')

admin.site.register(PerfilEstudiante, PerfilEstudianteAdmin)