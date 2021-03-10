from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('acoes/<str:codigo_da_acao>/<int:dias>', views.acoes, name='acoes'),
    path('acoes/<str:codigo_da_acao>/', views.acoes, name='acoes'),
    path('introducao', views.introducao, name='introducao'),
    path('tecnicas', views.tecnicas, name='tecnicas'),
    path('lista', views.lista, name='lista'),
    path('compare', views.comparacao, name='comparacao'),
    path('compare/<int:dias>', views.comparacao),
    path('sugestoes', views.sugestoes),
    path('perfil', views.perfil),
]