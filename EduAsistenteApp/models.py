from django.db import models
from django.core.exceptions import ValidationError
from EduEstudianteApp.models import PerfilEstudiante

class AssistantCollection(models.Model):
    Nombre_Coleccion = models.CharField(max_length=255, help_text='Ingresa el nombre de la colleccion para el asistente')

    #funcion para validar que solo se pueda ingresar una vez
    def save(self, *args, **kwargs):
        if self.pk is None and AssistantCollection.objects.exists():
            raise ValidationError('No puedes crear un nuevo registro de AssistantCollection. Solo puedes modificar el existente.')
        super(AssistantCollection, self).save(*args, **kwargs)

    def __str__(self):
        return self.Nombre_Coleccion

#modelo para guardar la pregunta del estudiante
class PreguntasEstudiante(models.Model):
    estudiante = models.ForeignKey(PerfilEstudiante, on_delete=models.CASCADE)
    preguntas = models.CharField(max_length=255, help_text='Ingresa la pregunta del estudiante')

    def __str__(self):
        return f'{self.estudiante.carnet} - {self.preguntas}'

#modelo para guardar la respuesta del asistente asicionada a la pregunta del estudiante
class RespuestasAsistenteEdula(models.Model):
    estudiante = models.ForeignKey(PerfilEstudiante, on_delete=models.CASCADE)
    preguntas = models.ForeignKey(PreguntasEstudiante, on_delete=models.CASCADE)
    respuesta = models.CharField(max_length=255, help_text='Ingresa la respuesta del asistente', null=True, blank=True)

    def __str__(self):
        return f'{self.estudiante.carnet} - {self.preguntas.preguntas} - {self.respuesta}'