from django.contrib import admin
from django.urls import path, include

from .views import BookView, SingleBookView, BookListView, profile, author_detail, home, AddBookToProfile

urlpatterns = [
    path('', home, name='home'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('api/book/', BookView.as_view(), name='api-book-list'),
    path('api/book/<int:pk>', SingleBookView.as_view()),
    path('api/add-book/', AddBookToProfile.as_view(), name='api-add-book'),
    path('books/<int:pk>/', SingleBookView.as_view(), name='book-detail'),
    path('profile/', profile, name='profile'),
    path('author/<int:author_id>/', author_detail, name='author_detail'),
]
