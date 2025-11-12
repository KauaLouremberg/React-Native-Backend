from rest_framework import serializers

from amparado.models import Amparado


class AmparadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amparado
        fields = '__all__'
        read_only_fields = ['usuario']