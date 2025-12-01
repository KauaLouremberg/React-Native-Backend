from rest_framework import serializers
from rest_framework.response import Response

from autenticacao.models import Usuario
from perfil.models import Perfil, Responsavel
from .models import AreaSegura, Marcadores


class AreaSeguraSerializer(serializers.ModelSerializer):
    center_lat = serializers.FloatField(write_only=True)
    center_lng = serializers.FloatField(write_only=True)
    radius = serializers.FloatField(write_only=True)

    class Meta:
        model = AreaSegura
        fields = [
            "id",
            "center_lat",
            "center_lng",
            "radius",
            "latitude",
            "longitude",
            "raio",
            "nome",
            "criado_em"
        ]
        read_only_fields = ["latitude", "longitude", "raio"]

    def create(self, validated_data):
        validated_data["latitude"] = validated_data.pop("center_lat")
        validated_data["longitude"] = validated_data.pop("center_lng")
        validated_data["raio"] = validated_data.pop("radius")
        validated_data["nome"] = validated_data.pop("nome")

        user = self.context["request"].user
        usuario = Usuario.objects.get(user=user)
        perfil = Perfil.objects.get(usuario=usuario)

        if usuario.is_amparado:
            return Response({'Erro!': "Usuario e um amparado!"})

        responsavel = Responsavel.objects.get(perfil=perfil)
        validated_data["responsavel_area"] = responsavel

        return AreaSegura.objects.create(**validated_data)

class MarcadoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marcadores
        fields = [
            "id",
            "nome",
            "latitude",
            "longitude",
            "criado_em",
        ]
        read_only_fields = ["id", "criado_em", "amparado"]
