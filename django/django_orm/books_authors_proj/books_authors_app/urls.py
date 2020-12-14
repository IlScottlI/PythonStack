from django.urls import path
from . import views

urlpatterns = [
    path('', views.books),
    path('authors/', views.authors),
    path('authors/<int:author_id>', views.authors_view),
    path('books/<int:book_id>', views.books_view),
    path('process/', views.process),
]
