from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('tasks/', views.task_list, name='task_list'),
    path('convert/', views.convert_device, name='convert_device'),
    path('tasks/ajouter/', views.ajouter_tache, name='ajouter_tache'),
    path('tasks/supprimer/<int:tache_id>/', views.supprimer_tache, name='supprimer_tache'),
    path('tasks/modifier/<int:tache_id>/', views.modifier_tache, name='modifier_tache'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
]