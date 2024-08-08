from django.contrib import admin
from django.urls import path, include

from .views import BookView, SingleBookView, BookListView, profile, author_detail, home

urlpatterns = [
    path('', home, name='home'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('api/book/', BookView.as_view(), name='book_list-api'),
    path('api/book/<int:pk>', SingleBookView.as_view()),
    path('profile/', profile, name='profile'),
    path('author/<int:author_id>/', author_detail, name='author_detail'),
]
