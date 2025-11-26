from rest_framework import serializers
from .models import Perfil, Endereco, Responsavel


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['id', 'cpf', 'data_nascimento', 'sexo', 'tipo_conta', 'apelido']
        read_only_fields = ['usuario']

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ['id', 'cidade', 'bairro', 'estado', 'cep', 'rua', 'numero']

class ResponsavelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel
        fields = '__all__'