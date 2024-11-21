from django.db import models
from django.contrib.auth.hashers import check_password, make_password

class PerfilEstudiante(models.Model):
    carnet = models.CharField(max_length=6, help_text='numero de carnet del estudiante', unique=True)
    password = models.CharField(max_length=128, help_text='contraseña del estudiante')

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def __str__(self):
        return f'Estudiante: {self.carnet}'