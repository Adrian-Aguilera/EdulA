from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password, make_password
# Create your models here.
class AssistantCollection(models.Model):
    Nombre_Coleccion = models.CharField(max_length=255, help_text='Ingresa el nombre de la colleccion para el asistente')

    #funcion para validar que solo se pueda ingresar una vez
    def save(self, *args, **kwargs):
        if self.pk is None and AssistantCollection.objects.exists():
            raise ValidationError('No puedes crear un nuevo registro de AssistantCollection. Solo puedes modificar el existente.')
        super(AssistantCollection, self).save(*args, **kwargs)

    def __str__(self):
        return self.Nombre_Coleccion

class Perfil(models.Model):
    carnet = models.CharField(max_length=6, help_text='numero de carnet del estudiante', unique=True)
    password = models.CharField(max_length=128, help_text='contraseña del estudiante')

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def __str__(self):
        return f'Estudiante: {self.carnet}'

class ChatHistory(models.Model):
    estudiante = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    conversation_id = models.IntegerField(null=True)
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('assistant', 'Assistant'), ('system', 'System')])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} - {self.content[:50]}"
