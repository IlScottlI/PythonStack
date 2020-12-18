from django.urls import path, include
from . import views
urlpatterns = [
    path('login/', views.login),
    path('process/', views.process),
    path('', views.index),
    path('logout/', views.logout),
    path('wall/', views.wall),
]
