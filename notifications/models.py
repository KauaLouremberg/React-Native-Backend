from django.db import models
from autenticacao.models import Usuario

class Device(models.Model):
    user_device = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="devices")
    fcm_token = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
