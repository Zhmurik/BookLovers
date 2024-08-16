from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book, Author, Profile
from .serializers import BookSerializer, AddBookToProfileSerializer, ProfileSerializer


class BookPagination(PageNumberPagination):
    page_size = 8


class BookView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination


class BookListView(TemplateView):
    template_name = 'book_list.html'


class SingleBookView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class SingleBookView(DetailView):
    model = Book
    template_name = 'single_book.html'
    context_object_name = 'book'


class ProfileView(APIView):
    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


# View to add a book to the user's profile by book title
@method_decorator(login_required, name='dispatch')
class AddBookToProfileView(APIView):
    def post(self, request):
        serializer = AddBookToProfileSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            book = serializer.save()
            return Response({
                'message': 'Book added to profile successfully.',
                'book': {
                    'title': book.title,
                    'author': book.author.name,
                    'published_date': book.published_date,
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
def profile_view(request):
    profile = request.user.profile
    read_books = profile.read_books.all()  # Fetch the books the user has read
    context = {
        'profile': profile,
        'read_books': read_books
    }
    return render(request, 'profile.html', context)


def author_list(request):
    authors = Author.objects.all()
    return render(request, 'author_list.html', {'authors': authors})


def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    return render(request, 'author_detail.html', {'author': author})


def home(request):
    context = {
        'username': request.user.username if request.user.is_authenticated else 'Guest'
    }
    return render(request, 'home.html', context)
