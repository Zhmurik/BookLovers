from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'genres', 'description', 'cover_image']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Show user details
    read_books = BookSerializer(many=True, read_only=True)  # Display books

    class Meta:
        model = Profile
        fields = ['user', 'read_books']


class AddBookToProfileSerializer(serializers.Serializer):
    title = serializers.CharField()

    def save(self, **kwargs):
        user = self.context.get('user')
        title = self.validated_data.get('title')

        try:
            book = Book.objects.get(title=title)
        except Book.DoesNotExist:
            raise serializers.ValidationError('Book not found.')

        # Add the book to the user's read_books
        profile = user.profile
        profile.read_books.add(book)
        return book
