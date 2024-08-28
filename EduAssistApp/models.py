from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class AssistantCollection(models.Model):
    nameCollection = models.CharField(max_length=255, help_text='Ingresa el nombre de la colleccion para el asistente')

    #funcion para validar que solo se pueda ingresar una vez
    def save(self, *args, **kwargs):
        if self.pk is None and AssistantCollection.objects.exists():
            raise ValidationError('No puedes crear un nuevo registro de AssistantCollection. Solo puedes modificar el existente.')
        super(AssistantCollection, self).save(*args, **kwargs)

    def __str__(self):
        return self.nameCollection