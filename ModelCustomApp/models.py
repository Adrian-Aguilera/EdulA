from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class SettingsLLM(models.Model):
    host = models.CharField(max_length=255, default='127.0.0.1:11434', help_text='Host de la conexion a ollama server, por defecto es 127.0.0.1:11434')
    Model_Embedding = models.CharField(max_length=255, default='mxbai-embed-large', help_text='Nombre del modelo que se usara para el embedding')
    def save(self, *args, **kwargs):
        if self.pk is None and SettingsLLM.objects.exists():
            raise ValidationError('No puedes crear un nuevo registro de SettingsLLM. Solo puedes modificar el existente.')
        super(SettingsLLM, self).save(*args, **kwargs)

    def __str__(self):
        return 'Configuracion LLM General'

class ModelsLLM(models.Model):
    Nombre = models.CharField(max_length=255, help_text='Nombre del modelo')
    model = models.CharField(max_length=255, help_text='Nombre del modelo')
    Is_Embedding = models.BooleanField(default=False, help_text='Si el modelo es un embedding')

    def __str__(self):
        return f'{self.Nombre} - {self.model}'
class SettingsChatGeneral(models.Model):
    Model_LLM = models.ForeignKey(ModelsLLM, on_delete=models.CASCADE, help_text='Modelo que se usara para el chat General')
    max_Tokens = models.IntegerField(unique=True, help_text='Maximo de tokens que generara la respuesta')
    temperature = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(1.0)
        ],
        help_text='Temperatura del modelo, entre 0 a 1'
    )
    num_gpu = models.IntegerField(unique=True, validators=[MinValueValidator(1), MaxValueValidator(100)], help_text='Numero de GPU que usara el modelo al generar respuesta (%)')

    def save(self, *args, **kwargs):
        if self.pk is None and SettingsChatGeneral.objects.exists():
            raise ValidationError('No puedes crear un nuevo registro de SettingsChatGeneral. Solo puedes modificar el existente.')
        super(SettingsChatGeneral, self).save(*args, **kwargs)

    def __str__(self):
        return 'Configuracion Chat General'

class SettingsChatAsistente(models.Model):
    Model_LLM = models.ForeignKey(ModelsLLM, on_delete=models.CASCADE, help_text='Modelo que se usara para el asistente del estudiante')
    max_Tokens = models.IntegerField(unique=True, help_text='Maximo de tokens que generara la respuesta')
    temperature = models.DecimalField(max_digits=2, decimal_places=2, default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], help_text='temperatura del modelo, entre 0 a 1')
    num_gpu = models.IntegerField(unique=True, validators=[MinValueValidator(1), MaxValueValidator(100)], help_text='Numero de GPU que usara el modelo al generar respuesta (%)')

    def save(self, *args, **kwargs):
        if self.pk is None and SettingsChatAsistente.objects.exists():
            raise ValidationError('No puedes crear un nuevo registro de SettingsChatAsistente. Solo puedes modificar el existente.')
        super(SettingsChatAsistente, self).save(*args, **kwargs)

    def __str__(self):
        return 'Configuracion Chat Asistente'


class SettingsChroma(models.Model):
    is_persistent = models.BooleanField(default=True, help_text='Si queremos que la db se sea persistente')
    persist_directory = models.CharField(max_length=255, default='./DB/Chroma_storageDB', help_text='Directorio donde se guardara la base de datos de vectorial (Chroma) en el sevo servidor')
    def save(self, *args, **kwargs):
        if self.pk is None and SettingsChroma.objects.exists():
            raise ValidationError('No puedes crear un nuevo registro de SettingsChroma. Solo puedes modificar el existente.')
        super(SettingsChroma, self).save(*args, **kwargs)

    def __str__(self):
        return 'Configuracion Chroma'