from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password, make_password
class AssistantCollection(models.Model):
    Nombre_Coleccion = models.CharField(max_length=255, help_text='Ingresa el nombre de la colleccion para el asistente')

    #funcion para validar que solo se pueda ingresar una vez
    def save(self, *args, **kwargs):
        if self.pk is None and AssistantCollection.objects.exists():
            raise ValidationError('No puedes crear un nuevo registro de AssistantCollection. Solo puedes modificar el existente.')
        super(AssistantCollection, self).save(*args, **kwargs)

    def __str__(self):
        return self.Nombre_Coleccion