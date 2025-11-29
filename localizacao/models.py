from django.db import models
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
