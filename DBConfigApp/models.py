from django.db import models

class DocumentosRagGeneral(models.Model):
    nombre = models.CharField(max_length=100, help_text='nombre del documento')
    documento = models.TextField(help_text='documentos que se usaran como contexto para el asistente')
    referencia_url = models.URLField(help_text='referencia url del documento', default='')

    def __str__(self):
        return f'{self.nombre}'

class DocumentosRagAsistente(models.Model):
    nombre = models.CharField(max_length=100, help_text='nombre del documento')
    documento = models.TextField(help_text='documentos que se usaran como contexto para el asistente')
    referencia_url = models.URLField(help_text='referencia url del documento', default='')

    def __str__(self):
        return f'{self.nombre}'