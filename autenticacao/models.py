from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    nome = models.CharField(max_length=150, blank=True, null=True)
    is_amparado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"
