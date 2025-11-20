from django.urls import path

from localizacao.views import LocalizacaoView

urlpatterns = [
    path('localizacao/', LocalizacaoView.as_view(), name='localizacao'),
]