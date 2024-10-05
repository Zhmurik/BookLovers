from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Book, Author, Tag, UserBook


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
    user = UserSerializer(read_only=True)
    read_books = BookSerializer(many=True, read_only=True)

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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'tag_name']


class UserBookSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    book_title = BookSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(required=True)

    class Meta:
        model = UserBook
        fields = ['book', ' book_title', 'tags', 'note', 'rating']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        user_book = UserBook.objects.create(**validated_data)

        for tag_data in tags_data:
            tag_name = tag_data.get('name')
            tag, created = Tag.objects.get_or_create(name=tag_name)
            user_book.tags.add(tag)

        return user_book

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        instance.note = validated_data.get('note', instance.note)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()

        if tags_data:
            instance.tags.clear()
            for tag_data in tags_data:
                tag_name = tag_data.get('name')
                tag, created = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)

        return instance
