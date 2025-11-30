from django.urls import path

from localizacao.views import LocalizacaoView, AreaSeguraListCreateView, LocalizacaoAmparadoView, MarcadoresView, \
    MarcadorDetailView

urlpatterns = [
    path('localizacao/', LocalizacaoView.as_view(), name='localizacao'),
    path('areas/', AreaSeguraListCreateView.as_view(), name='areas'),
    path('geofencing/', LocalizacaoAmparadoView.as_view(), name='geofencing'),
    path('marcadores/', MarcadoresView.as_view(), name='marcadores'),
    path('marcadores/<int:id>/', MarcadorDetailView.as_view(), name='marcador-detail'),
]