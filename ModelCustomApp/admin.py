from django.contrib import admin
from .models import SettingLLM, SettingsChatGeneral, SettingsChatAsistente, SettingsChroma, ModelsLLM
# Register your models here.

admin.site.register(SettingLLM)
admin.site.register(SettingsChatGeneral)
admin.site.register(SettingsChatAsistente)
admin.site.register(SettingsChroma)
admin.site.register(ModelsLLM)