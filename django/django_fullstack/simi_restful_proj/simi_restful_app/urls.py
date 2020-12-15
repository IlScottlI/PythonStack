from django.urls import path
from . import views

urlpatterns = [
    path('shows', views.shows),
    path('shows/new', views.new),
    path('shows/<int:show_id>', views.view),
    path('shows/<int:show_id>/edit', views.edit),
    path('shows/<int:show_id>/destroy', views.destroy),
    path('process/', views.process),
]
