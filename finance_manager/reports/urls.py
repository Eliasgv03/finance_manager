# reports/urls.py
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('report/', views.generate_report, name='generate_report'),
    path('report-content/', views.report_content, name='report_content'), # Nueva URL para HTMX
]
