import random

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from rest_framework import generics, status, viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book, Author, Profile, Rating, UserBook
from .serializers import BookSerializer, AddBookToProfileSerializer, ProfileSerializer, UserBookSerializer


class BookPagination(PageNumberPagination):
    page_size = 8


class BookView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def get_queryset(self):
        queryset = Book.objects.all()
        search_query = self.request.query_params.get('search', '')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        return queryset


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        return queryset


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


@login_required(login_url='/login/')
def profile_view(request):
    profile = request.user.profile
    read_books = profile.read_books.all()
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
    books = Book.objects.order_by('?')[:6]
    recommended_books = recommend_books(request.user)
    random.shuffle(recommended_books)
    context = {
        'recommended_books': recommended_books[:4],
        'username': request.user.username if request.user.is_authenticated else 'Guest',
        'books': books
    }
    return render(request, 'home.html', context)


class BookSearchView(ListView):
    model = Book
    template_name = 'book_search_results.html'
    context_object_name = 'books'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Book.objects.filter(
                Q(title__icontains=query) | Q(author__name__icontains=query)
            )
        return Book.objects.none()


def recommend_books(user):
    profile = user.profile
    read_books = profile.read_books.all()
    read_authors = []
    for book in read_books:
        read_authors.append(book.author)
    recommended_books = []
    for author in read_authors:
        author_books = Book.objects.filter(author=author)
        for book in author_books:
            if book not in read_books:
                recommended_books.append(book)

    return recommended_books


class UserBookViewSet(viewsets.ModelViewSet):
    serializer_class = UserBookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_profile = self.user.profile
        return UserBook.objects.filter(user_profile=user_profile)

    def perform_create(self, serializer):
        user_profile = self.request.user.profile
        serializer.save(user_profile=user_profile)

    def perform_update(self, serializer):
        serializer.save






# def get_similar_users(user):
#     ratings = Rating.objects.filter(user=user)
#     similar_users = {}
#
#     for rating in ratings:
#         same_book_ratings = Rating.objects.filter(book=rating.book).exclude(user=user)
#         for r in same_book_ratings:
#             if r.user in similar_users:
#                 similar_users[r.user] +=1
#             else:
#                 similar_users[r.user] = 1
#     similar_users = sorted(similar_users.items(), key=lambda x: x[1], reverse=True)
#     return [user for user, count in similar_users]
#
#
# def recommend_books(user):
#     similar_users = get_similar_users(user)
#     recommended_books = set()
#
#     for similar_user in similar_users:
#         rating = Rating.objects.filter(user=similar_user).order_by('-rating')
#         for rating in rating:
#             if rating.book not in recommended_books and not Rating.objects.filter(user=user, book=rating.book).existst():
#                 recommended_books.add(rating.book)
#                 if len(recommended_books) >= 6:
#                     break
#         if len(recommended_books) >= 6:
#             break
#     return list(recommended_books)
#
#


