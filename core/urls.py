from django.urls import path
from . import views
from . import views_painel

app_name = 'core'

urlpatterns = [
    # Site Público
    path('', views.home, name='home'),

    # Painel Administrativo Amigável
    path('painel/login/', views_painel.painel_login, name='painel_login'),
    path('painel/logout/', views_painel.painel_logout, name='painel_logout'),
    path('painel/', views_painel.painel_dashboard, name='painel_dashboard'),

    # Gestão de Animais
    path('painel/animais/', views_painel.animal_list, name='animal_list'),
    path('painel/animais/novo/', views_painel.animal_create, name='animal_create'),
    path('painel/animais/<str:animal_id>/editar/', views_painel.animal_edit, name='animal_edit'),
    path('painel/animais/<str:animal_id>/excluir/', views_painel.animal_delete, name='animal_delete'),

    # Gestão de Patrocinadores
    path('painel/patrocinadores/', views_painel.patrocinador_list, name='patrocinador_list'),
    path('painel/patrocinadores/novo/', views_painel.patrocinador_create, name='patrocinador_create'),
    path('painel/patrocinadores/<str:patrocinador_id>/excluir/', views_painel.patrocinador_delete, name='patrocinador_delete'),

    # Solicitações de Adoção
    path('painel/adocoes/', views_painel.adocao_list, name='adocao_list'),
]
