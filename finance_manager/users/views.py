from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import RegisterForm, LoginForm, EditProfileForm




def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"Intentando autenticar: {username} con {password}")  # Depuración

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect('profile')
            else:
                print("Autenticación fallida")  # Más depuración
        return render(request, 'users/login.html', {'form': form, 'error': 'Invalid credentials'})
    return render(request, 'users/login.html', {'form': LoginForm()})




def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    balance = profile.initial_balance  # Supongo que tienes un campo `balance` en el perfil
    return render(request, 'users/profile.html', {'profile': profile, 'balance': balance})
   
@login_required
def edit_profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'users/edit_profile.html', {'form': form})

