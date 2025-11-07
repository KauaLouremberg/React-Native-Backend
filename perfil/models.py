from django.db import models
from django.contrib.auth.models import User

from autenticacao.models import Usuario


class Perfil(models.Model):
    TIPO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outros')
    )

    TIPO_MODERACAO = (
        ('A', 'Administrador'),
        ('U', 'Usuario'),
    )

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='perfil_user')
    cpf = models.CharField(max_length=14, blank=True, null=True)
    data_nascimento = models.DateTimeField(blank=True, null=True)
    sexo = models.CharField(choices=TIPO_CHOICES, max_length=1, blank=True, null=True)
    tipo_conta = models.CharField(choices=TIPO_MODERACAO, max_length=1, blank=True, null=True)

class Endereco(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='endereco')
    estado = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=255, blank=True, null=True)
    rua = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)

