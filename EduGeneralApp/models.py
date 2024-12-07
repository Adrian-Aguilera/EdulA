from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
class General_Collection(models.Model):
    Nombre_Coleccion = models.CharField(max_length=255, help_text='Ingresa el nombre de la colleccion para chat general')

    #funcion para validar que solo se pueda ingresar una vez
    def save(self, *args, **kwargs):
        if self.pk is None and General_Collection.objects.exists():
            raise ValidationError('Solo puedes crear una coleccion para el asistente General.')
        super(General_Collection, self).save(*args, **kwargs)

    def __str__(self):
        return self.Nombre_Coleccion


class DataFileOption(models.Model):
    fileName = models.CharField(max_length=255, help_text="nombre del archivo...", default='')
    filePDF = models.FileField(upload_to='EduApp/static/')
    def __str__(self):
        return self.fileName