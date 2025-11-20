from rest_framework.response import Response

from .models import Usuario
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'is_amparado']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['username'] = self.user.username
        data['email'] = self.user.email
        data['is_superuser'] = self.user.is_superuser

        criar, _ = Usuario.objects.update_or_create(user=self.user, nome=self.user.username)
        return data

class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    is_superuser = serializers.BooleanField(default=False)

    def create(self, validated_data):
        is_super = validated_data.pop("is_superuser")

        try:
            if is_super:
                user = User.objects.create_superuser(**validated_data)
            else:
                user = User.objects.create_user(**validated_data)
        except:
            return Response({"Erro!": "Ja existe um usuario registrado!"})

        return user

