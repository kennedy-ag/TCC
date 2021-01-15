from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('acoes/<str:codigo_da_acao>/<int:dias>', views.acoes, name='acoes'),
]