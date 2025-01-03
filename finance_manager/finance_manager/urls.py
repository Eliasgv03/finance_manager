"""
URL configuration for finance_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('users/login')  # 'login' debe ser el nombre de tu vista de inicio de sesión

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('tags/', include('tags.urls')),
    path('currencies/', include('currencies.urls')),
    path('transactions/', include('transactions.urls')),
    path('', redirect_to_login),  # Redirigir al inicio de sesión por defecto
   
]
