from rest_framework import serializers
from .models import Book


class BookDetailSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Book
        fields = '__all__'

    def save(self, **kwargs):
        user = self.context.get('users')
        if user:
            book_id = self.validated.data['book_id']
            if book_id:
                try:
                    book = Book.objects.get(id=book_id)
                    user.profile.read_books.add(book)
                except Book.DoesNotExist:
                    raise serializers.ValidationError('Book not found.')
        return super().save(**kwargs)


