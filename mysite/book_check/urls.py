from django.contrib import admin
from django.urls import path, include

from .views import (BookView, SingleBookView, BookListView, ProfileView, author_detail,
                    home, AddBookToProfileView, profile_view, author_list)

urlpatterns = [
    path('', home, name='home'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('api/book/', BookView.as_view(), name='api-book-list'),
    path('api/book/<int:pk>', SingleBookView.as_view()),
    path('api/add-book/', AddBookToProfileView.as_view(), name='api-add-book'),
    path('books/<int:pk>/', SingleBookView.as_view(), name='book-detail'),
    path('api/profile/', ProfileView.as_view(), name='api-profile'),
    path('profile/', profile_view, name='profile'),
    path('author/<int:author_id>/', author_detail, name='author_detail'),
    path('authors/', author_list, name='author-list')
]
