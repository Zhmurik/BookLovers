from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from rest_framework import generics

from .models import Book, Author
from .serializers import BookDetailSerializer


class BookView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer


class BookListView(TemplateView):
    template_name = 'book_list.html'


class SingleBookView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer

@login_required
def profile(request):
    profile = request.user.profile
    read_books = profile.read_books.all()
    return render(request, 'profile.html', {'profile': profile, 'read_books': read_books})


def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    return render(request, 'author_detail.html', {'author': author})


def home(request):
    return render(request, 'home.html')
