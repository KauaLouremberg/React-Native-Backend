from rest_framework import serializers
from .models import Perfil, Endereco


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['id', 'cpf', 'data_nascimento', 'sexo', 'tipo_conta']
        read_only_fields = ['usuario']

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ['id', 'cidade', 'bairro', 'estado']
