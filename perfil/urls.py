from rest_framework.routers import DefaultRouter
from .views import PerfilViewSet, EnderecoViewSet

router = DefaultRouter()
router.register(r'perfil', PerfilViewSet)
router.register(r'endereco', EnderecoViewSet)

urlpatterns = router.urls