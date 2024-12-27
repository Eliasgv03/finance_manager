
# currencies/urls.py
from django.urls import path
from . import views

app_name = 'currencies'

urlpatterns = [
    path('convertir/', views.convert_view, name='convertir'),
]