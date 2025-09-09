import os
import requests
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Tasks
from .forms import TaskForm

@login_required
def ajouter_tache(request):
    error = None
    if request.method == 'POST':
        titre = request.POST.get('titre')
        date = request.POST.get('date') or None
        heure = request.POST.get('heure') or None

        if titre:
            now = datetime.now()
            if date and heure:
                try:
                    dt_str = f"{date} {heure}"
                    dt_obj = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
                    if dt_obj < now:
                        error = "La date et l'heure ne peuvent pas être dans le passé."
                except ValueError:
                    error = "Date ou heure invalide."
            elif date:
                try:
                    dt_obj = datetime.strptime(date, "%Y-%m-%d")
                    if dt_obj.date() < now.date():
                        error = "La date ne peut pas être dans le passé."
                except ValueError:
                    error = "Date invalide."
            elif heure:
                error = "Veuillez spécifier une date avec l'heure."

            if not error:
                Tasks.objects.create(titre=titre, date=date, heure=heure)
                return redirect('task_list')

    return redirect(f"{request.META.get('HTTP_REFERER')}?error={error}" if error else 'task_list')

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
    error = request.GET.get("error")
    return render(request, 'task_list.html', {'task_forms': task_forms, 'error': error})

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
            cleaned_date = form.cleaned_data.get('date')
            cleaned_heure = form.cleaned_data.get('heure')
            now = datetime.now()
            if cleaned_date and cleaned_heure:
                dt_obj = datetime.combine(cleaned_date, cleaned_heure)
                if dt_obj < now:
                    return render(request, 'task_update.html', {'form': form, 'tache': tache, 'error': "Date/heure dans le passé."})
            elif cleaned_date:
                if cleaned_date < now.date():
                    return render(request, 'task_update.html', {'form': form, 'tache': tache, 'error': "Date dans le passé."})
            elif cleaned_heure:
                return render(request, 'task_update.html', {'form': form, 'tache': tache, 'error': "Veuillez spécifier une date avec l'heure."})
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=tache)
    return render(request, 'task_update.html', {'form': form, 'tache': tache})
