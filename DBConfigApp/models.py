from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class DataGeneralChat(models.Model):
    dataContent = models.TextField(help_text='datos que se usaran como contexto para General chat')
    def save(self, *args, **kwargs):
        if self.pk is None and DataGeneralChat.objects.exists():
            raise ValidationError('No puedes crear un nuevo campo campo para el contenido de chatGeneral')
        super(DataGeneralChat, self).save(*args, **kwargs)

    def __str__(self):
        return self.dataContent

class DataAsistenteChat(models.Model):
    dataContent = models.TextField(help_text='datos que se usaran como contexto para el asistente')
    def save(self, *args, **kwargs):
        if self.pk is None and DataAsistenteChat.objects.exists():
            raise ValidationError('No puedes crear un nuevo campo campo para el contenido del asistente')
        super(DataAsistenteChat, self).save(*args, **kwargs)

    def __str__(self):
        return self.dataContent
