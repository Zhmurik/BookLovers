from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book-list'),
    path('books/<int:pk>/', views.single_book, name='book-detail'),
    path('profile/', views.profile, name='profile'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('authors/', views.author_list, name='author-list'),
    path('books/search/', views.book_search, name='book-search'),
]

urlpatterns += router.urls
