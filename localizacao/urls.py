from django.urls import path

from localizacao.views import LocalizacaoView, AreaSeguraListCreateView, LocalizacaoAmparadoView

urlpatterns = [
    path('localizacao/', LocalizacaoView.as_view(), name='localizacao'),
    path('areas/', AreaSeguraListCreateView.as_view(), name='areas'),
    path('geofencing/', LocalizacaoAmparadoView.as_view(), name='geofencing')
]