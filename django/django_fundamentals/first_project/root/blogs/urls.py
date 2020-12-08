from django.urls import path
from . import views

urlpatterns = [
    path('', views.root),
    path('index/', views.index),
    path('blogs/', views.blogs),
    path('blogs/new/', views.new),
    path('blogs/create/', views.create),
    path('blogs/<int:number>/', views.view),
    path('blogs/<int:number>/edit', views.edit),
    path('blogs/<int:number>/delete', views.destroy),
    path('blogs/json/', views.return_json),
]
