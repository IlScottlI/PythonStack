from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('destroy_session', views.destroy_session),
    path('plus_two', views.plus_two),
    path('setIncrement', views.setIncrement),
]
