from django.contrib import admin
from django.urls import path, include

from .views import BookCreateView

urlpatterns = [
    path('', BookCreateView.as_view()),
]
