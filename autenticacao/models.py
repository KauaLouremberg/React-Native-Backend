from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    ROLE_CHOICES = (
        ('usuario', 'Usuário'),
        ('moderador', 'Moderador'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    perfil = models.CharField(max_length=20, choices=ROLE_CHOICES, default='usuario')
    nome = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.perfil})"
