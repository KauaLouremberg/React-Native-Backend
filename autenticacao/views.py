from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Usuario
from .serializers import UsuarioSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class UsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = Usuario.objects.get(user=request.user)
        serializer = UsuarioSerializer(usuario)

        if request.query_params.get("perfil"):
            return Response(usuario.perfil)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        perfil = data.get("perfil")

        perfil_update = Usuario.objects.update(perfil=perfil)
        return Response(perfil_update)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer