import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tasks
from .forms import TaskForm
from django.contrib.auth import logout

@login_required
def ajouter_tache(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        date = request.POST.get('date') or None
        heure = request.POST.get('heure') or None

        if titre:
            Tasks.objects.create(titre=titre, date=date, heure=heure)
        return redirect('task_list')

@login_required
def deconnexion(request):
    logout(request)
    return redirect('login')

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
def accueil(request):
    return render(request, 'accueil.html')

@login_required
def task_list(request):
    tasks = Tasks.objects.all()
    task_forms = [(task, TaskForm(instance=task)) for task in tasks]
    return render(request, 'task_list.html', {'task_forms': task_forms})

@login_required
def convert_device(request):
    exchange_rates = get_exchange_rates()
    return render(request, 'convert_device.html', {'exchange_rates': exchange_rates})

@login_required
def supprimer_tache(request, tache_id):
    tache = get_object_or_404(Tasks, id=tache_id)
    tache.delete()
    return redirect('task_list')

@login_required
def modifier_tache(request, tache_id):
    tache = get_object_or_404(Tasks, id=tache_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=tache)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=tache)
    return render(request, 'task_update.html', {'form': form, 'tache': tache})