from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

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


class SingleBookView(DetailView):
    model = Book
    template_name = 'single_book.html'
    context_object_name = 'book'


class AddBookToProfile(APIView):
    def post(self, request):
        serializer = BookDetailSerializer(data=request.data, context={'users': request.user})
        if serializer.is_valid():
            serializer.save()
            book_id = serializer.validated_data.get('book_id')
            book = Book.objects.get(id=book_id)
            return Response({'message': 'Book added to profile successfully.',
                             'book': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
