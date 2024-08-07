from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class DataChromaGeneral(models.Model):
    dataContent = models.TextField(help_text='datos que se usaran como contexto para General chat')
    def save(self, *args, **kwargs):
        if self.pk is None and DataChromaGeneral.objects.exists():
            raise ValidationError('No puedes crear un nuevo campo campo para el contenido de chatGeneral')
        super(DataChromaGeneral, self).save(*args, **kwargs)

    def __str__(self):
        return self.dataContent
