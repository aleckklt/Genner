from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='accueil'),
    path('ajouter/', views.ajouter_tache, name='ajouter_tache'),
    path('modifier/<int:tache_id>/', views.modifier_tache, name='modifier_tache'),
    path('supprimer/<int:tache_id>/', views.supprimer_tache, name='supprimer_tache'),
]