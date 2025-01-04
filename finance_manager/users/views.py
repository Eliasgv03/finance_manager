from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile, Currency
from .forms import RegisterForm, LoginForm, EditProfileForm
from django.contrib import messages
import requests
from django.conf import settings
from django.contrib.messages import get_messages


def login_view(request):
    if request.user.is_authenticated:
        return redirect('users:profile')
   
    storage = get_messages(request)
    list(storage)  
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('users:profile')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, 'users/login.html', {'form': LoginForm()})



def logout_view(request):
    logout(request)
    return redirect('users:login')

def register_view(request):
    
    if request.user.is_authenticated:
        return redirect('users:profile')
    
    storage = get_messages(request)
    list(storage)  # Forzar iteración para limpiar mensajes antiguos
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully. Welcome!")
            return redirect('users:profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    balance = profile.initial_balance 
    return render(request, 'users/profile.html', {'profile': profile, 'balance': balance})
   

@login_required
def edit_initial_balance_view(request):
    profile = request.user.profile
    currencies = Currency.objects.all()
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('users:profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EditProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {
        'form': form,
        'currencies': currencies,
    })
