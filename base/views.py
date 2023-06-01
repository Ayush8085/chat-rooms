from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm

# Create your views here.

def home(request):
    context = {}
    return render(request, 'index.html', context)

def registerUser(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/register.html', context)