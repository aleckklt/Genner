import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tasks
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
import requests
import os

def get_exchange_rates():
    api_key = os.getenv('API_KEY')
    if not api_key:
        return {}
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('result') == 'success':
            return data.get('conversion_rates', {})
    return {}

@login_required
def article_list(request):
    tasks = Tasks.objects.all()
    tasks_data = [
        {
            'id': t.id,
            'titre': t.titre,
            'statut': t.statut,
            'date': t.date.strftime('%Y-%m-%d') if t.date else '',
            'heure': t.heure.strftime('%H:%M') if t.heure else '',
        }
        for t in tasks
    ]
    exchange_rates = get_exchange_rates()
    exchange_rates_json = json.dumps(exchange_rates)
    return render(request, 'gestionneur_task/task_list.html', {
        'tasks': tasks,
        'tasks_data': tasks_data,
        'exchange_rates': exchange_rates_json,
    })

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
        form = TaskForm(request.POST, instance=tache)
        if form.is_valid():
            form.save()
            return redirect('accueil')
    else:
        form = TaskForm(instance=tache)
    return render(request, 'gestionneur_task/task_update.html', {
        'form': form,
        'tache': tache
    })