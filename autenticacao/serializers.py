from .models import Usuario
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'perfil', 'nome']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['is_superuser'] = self.user.is_superuser

        criar, _ = Usuario.objects.update_or_create(user=self.user, nome=self.user.username)
        return data
