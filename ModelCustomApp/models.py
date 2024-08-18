from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class SettingsLLMGeneral(models.Model):
    host = models.CharField(max_length=255, help_text='Host de la conexion a ollama server')
    max_Tokens = models.IntegerField(unique=True, help_text='Maximo de tokens que generara la respuesta')
    temperature = models.DecimalField(max_digits=2, decimal_places=2, default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], help_text='temperatura del modelo, entre 0 a 1')
    num_gpu = models.IntegerField(unique=True, validators=[MinValueValidator(1), MaxValueValidator(100)], help_text='Numero de GPU que usara el modelo al generar respuesta')

    def save(self, *args, **kwargs):
        if self.pk is None and SettingsLLMGeneral.objects.exists():
            raise ValidationError('No puedes crear un nuevo registro de SettingsLLMGeneral. Solo puedes modificar el existente.')
        super(SettingsLLMGeneral, self).save(*args, **kwargs)

    def __str__(self):
        return 'Configuracion LLM General'