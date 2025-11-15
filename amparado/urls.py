from django.urls import path
from .views import AmparadoView, AmparadoCodigoView

urlpatterns = [
    path('amparado/', AmparadoView.as_view(), name='amparado'),
    path('ampcodigo/', AmparadoCodigoView.as_view(), name='codamparado')
]