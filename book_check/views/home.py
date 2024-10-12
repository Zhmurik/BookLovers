import random

from django.shortcuts import render

from ..models import Book


def home(request):
    """
        Shows the home page with books.
        If the user is registered, he sees a recommendation list for future reading.
    """
    books = Book.objects.order_by('?')[:6]
    if not request.user.is_authenticated:
        context = {
            'username': request.user.username if request.user.is_authenticated else 'Guest',
            'books': books
        }
        return render(request, 'home.html', context)
    recommended_books = recommend_books(request.user)
    random.shuffle(recommended_books)
    context = {
        'recommended_books': recommended_books[:4],
        'username': request.user.username if request.user.is_authenticated else 'Guest',
        'books': books
    }
    return render(request, 'home.html', context)

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