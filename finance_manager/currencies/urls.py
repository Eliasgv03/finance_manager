
# currencies/urls.py
from django.urls import path
from . import views

app_name = 'currencies'

urlpatterns = [
    path('convert/', views.convert_view, name='convert'),
]