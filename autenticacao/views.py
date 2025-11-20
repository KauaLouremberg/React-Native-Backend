from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Usuario
from .serializers import UsuarioSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, UserCreateSerializer

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
    permission_classes = [AllowAny]

    serializer_class = CustomTokenObtainPairSerializer

class CreateUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = UserCreateSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({"Sucesso!": {f"Usuario Criado com Sucesso!"}})

        return Response({"Erro!": "Ocorreu um erro ao criar o usuario!"})

