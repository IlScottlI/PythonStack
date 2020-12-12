from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('guess/', views.guess),
    path('clean/', views.clearSession),
    path('submit/', views.submitResults),
    path('leaderboard/', views.leaderboard),
]
