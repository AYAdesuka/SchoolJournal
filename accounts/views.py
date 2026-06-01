from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm, LoginForm


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:home')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main:home')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def my_profile(request):
    user = request.user
    context = {
        'user': user,
        'role': user.role,
    }
    return render(request, 'my_profile.html', context)
