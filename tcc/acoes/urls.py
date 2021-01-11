from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('previsoes/<str:codigo_da_acao>', views.previsoes, name='previsoes'),
]