from django.urls import path
from .views import AmparadoViewSet, AmparadoCodigoViewSet

urlpatterns = [
    path('amparado/', AmparadoViewSet.as_view(), name='amparado'),
    path('ampcodigo/', AmparadoCodigoViewSet.as_view(), name='codamparado')
]