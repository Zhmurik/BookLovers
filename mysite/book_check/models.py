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

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    tag_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class UserBook(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    note = models.TextField(blank=True, null=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                              null=True, blank=True)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.book.title}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.user.username} - {self.book.title}: {self.rating}'
