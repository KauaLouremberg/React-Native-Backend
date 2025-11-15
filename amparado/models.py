from django.db import models

from autenticacao.models import Usuario

class Amparado(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="amparado_usuario")
    responsavel = models.ForeignKey('perfil.Responsavel', on_delete=models.CASCADE, related_name="responsavel_amparado", null=True)
    codigo_convite = models.CharField(max_length=8, blank=True, null=True)
