from rest_framework import generics
from .serializers import BookDetailSerializer


class BookCreateView(generics.CreateAPIView):
    serializer_class = BookDetailSerializer
