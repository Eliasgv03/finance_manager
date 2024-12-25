# tags/urls.py
from django.urls import path
from . import views

app_name = 'tags'

urlpatterns = [
    path('', views.list_tags, name='list_tags'),
    path('create/', views.create_tag, name='create_tag'),
    path('<int:tag_id>/edit/', views.edit_tag, name='edit_tag'),
    path('<int:tag_id>/delete/', views.delete_tag, name='delete_tag'),
]
