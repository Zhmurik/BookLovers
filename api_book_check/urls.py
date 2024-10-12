from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (BookAPIView, SingleBookAPIView, ProfileAPIView, AddBookToProfileView)


urlpatterns = [
    path('api/book/', BookAPIView.as_view(), name='api-book-list'),
    path('api/book/<int:pk>', SingleBookAPIView.as_view()),
    path('api/add-book/', AddBookToProfileView.as_view(), name='api-add-book'),
    path('api/profile/', ProfileAPIView.as_view(), name='api-profile'),
]

