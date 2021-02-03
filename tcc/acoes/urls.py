from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('acoes/<str:codigo_da_acao>/<int:dias>', views.acoes, name='acoes'),
    path('acoes/<str:codigo_da_acao>/', views.acoes, name='acoes'),
    path('teste/<str:codigo_da_acao>/<int:dias>', views.teste, name='teste'),
]