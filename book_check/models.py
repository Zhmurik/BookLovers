from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Book name', db_index=True,)
    author = models.ForeignKey(Author, related_name='books', verbose_name='Author', on_delete=models.CASCADE)
    published_date = models.CharField(max_length=30, verbose_name='Originally published',)
    GENRES_TYPES = (
        (1, 'Classics'),
        (2, 'Action and Adventure'),
        (3, 'Fantasy'),
        (4, 'Horror'),
        (5, 'Novel'),
        (6, 'Historical Fiction'),
        (7, 'Dystopian'),
        (8, 'Detective and Mystery')
    )
    genres = models.IntegerField(verbose_name='Genres', choices=GENRES_TYPES,)
    description = models.TextField(verbose_name='Book description')
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)

    def __str__(self):
        return f'"{self.title}" -  {self.author.name}'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                )
    read_books = models.ManyToManyField('Book', blank=True)

    def is_read(self, book: Book):
        return book in self.read_books.all()

    def add_book(self, book: Book):
        if not self.is_read(book):
            self.read_books.add(book)
            self.save()

    def __str__(self):
        return self.user.username


class UserBookInteraction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    tags = models.CharField(max_length=50, blank=True)
    note = models.TextField(blank=True, null=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                              null=True, blank=True)

    class Meta:
        unique_together = ('profile', 'book')

    def get_user_rating(self, book: Book, profile: Profile):
        return self.rating

    def set_rating(self, new_rating):
        self.rating = new_rating
        self.save()

    @classmethod
    def get_or_none(cls, profile: Profile, book: Book):
        try:
            return cls.objects.get(profile=profile, book=book)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_rating_or_none(cls, profile: Profile, book: Book):
        try:
            return cls.objects.get(profile=profile, book=book).rating
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return f"{self.profile.user.username} - {self.book.title}"

