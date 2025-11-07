from rest_framework import serializers
from .models import Usuario

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'perfil', 'usuario', 'cpf']

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'cidade', 'bairro', 'estado']
