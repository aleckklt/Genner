from django.shortcuts import render, redirect, get_object_or_404
from .models import Tasks
from django.contrib.auth.decorators import login_required

@login_required
def article_list(request):
    tasks = Tasks.objects.all()
    return render(request, 'gestionneur_task/task_list.html', {'tasks': tasks})

@login_required
def ajouter_tache(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        date = request.POST.get('date')
        heure = request.POST.get('heure')
        if titre:
            Tasks.objects.create(titre=titre, date=date, heure=heure)
    return redirect('accueil')

@login_required
def supprimer_tache(request, tache_id):
    tache = get_object_or_404(Tasks, id=tache_id)
    tache.delete()
    return redirect('accueil')

@login_required
def modifier_tache(request, tache_id):
    tache = get_object_or_404(Tasks, id=tache_id)
    if request.method == 'POST':
        nouveau_titre = request.POST.get('titre')
        if nouveau_titre:
            tache.titre = nouveau_titre
            tache.save()
            return redirect('accueil')
    return render(request, 'gestionneur_task/task_update.html', {'tache': tache})
