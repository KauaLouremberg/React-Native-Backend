from django.db import models

from amparado.models import Amparado
from perfil.models import Responsavel

class AreaSegura(models.Model):
    responsavel_area = models.ForeignKey(Responsavel, on_delete=models.CASCADE)

    latitude = models.FloatField()
    longitude = models.FloatField()
    raio = models.FloatField()

    nome = models.CharField(max_length=100, default="Área Segura")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - Resp {self.responsavel_area.id}"

class Marcadores(models.Model):
    amparado_markers = models.ForeignKey(Amparado, on_delete=models.CASCADE)

    nome = models.CharField(max_length=255, default="Marcador")
    latitude = models.FloatField()
    longitude = models.FloatField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome or f"Marcador em {self.latitude}, {self.longitude}"
