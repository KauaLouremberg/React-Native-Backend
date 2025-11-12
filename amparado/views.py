import uuid

from rest_framework.response import Response
from rest_framework.views import APIView

from amparado.models import Amparado


class AmparadoViewSet(APIView):

    def get(self):
        print('teste')


class AmparadoCodigoViewSet(APIView):

    def get(self, request):
        id = str(uuid.uuid4())[:8].upper()

        amparado = Amparado.objects.get(usuario__user__id=request.user.id)
        amparado.codigo_convite = id
        amparado.save()

        return Response(id)






