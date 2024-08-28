from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
class NameCollectionGeneral(models.Model):
    nameCollection = models.CharField(max_length=255, help_text='Ingresa el nombre de la colleccion para chat general')

    #funcion para validar que solo se pueda ingresar una vez
    def save(self, *args, **kwargs):
        if self.pk is None and NameCollectionGeneral.objects.exists():
            raise ValidationError('No puedes crear un nuevo registro de ConfigGeneral. Solo puedes modificar el existente.')
        super(NameCollectionGeneral, self).save(*args, **kwargs)

    def __str__(self):
        return self.nameCollection


class DataFileOption(models.Model):
    fileName = models.CharField(max_length=255, help_text="nombre del archivo...", default='')
    filePDF = models.FileField(upload_to='EduApp/static/')
    def __str__(self):
        return self.fileName