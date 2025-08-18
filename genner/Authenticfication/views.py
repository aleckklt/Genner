from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm

def login_view(request):
    error = False
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('accueil')
        else:
            error = True
    return render(request, "authenticfication/login.html", {"error": error})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accueil')
        else:
            return render(request, 'authenticfication/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'authenticfication/register.html', {'form': form})