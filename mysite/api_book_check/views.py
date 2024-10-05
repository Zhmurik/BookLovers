from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from mysite.book_check.models import Book, Profile
from mysite.book_check.serializers import BookSerializer, ProfileSerializer, AddBookToProfileSerializer


class BookAPIView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating Books.
    """
    class BookPagination(PageNumberPagination):
        page_size = 8
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def get_queryset(self):
        queryset = Book.objects.all()
        search_query = self.request.query_params.get('search', '')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        return queryset


class SingleBookAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for concrete view for retrieving or deleting a book instance.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ProfileAPIView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for displaying information about the user and his read books.
    """

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.all()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(login_required, name='dispatch')
class AddBookToProfileView(APIView):
    """
    API endpoint for adding book in user`s profile.
    """
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