from warnings import catch_warnings

from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from ..forms import UserBookForm
from ..models import Book, UserBookInteraction


def single_book(request, pk):
    """
        Shows page with a single book in the library.
    """
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'GET':
        allow_add = True

        if request.user.is_authenticated and request.user.profile.is_read(book):
            allow_add = False
        return TemplateResponse(request, "single_book.html", {
            "book": book,
            "allow_add": allow_add,
            "is_authenticated": request.user.is_authenticated,
        })
    elif request.method == 'POST' and request.user.is_authenticated:
        profile = request.user.profile
        if 'book_id' in request.POST:
            profile.add_book(book)
            messages.success(request, 'The book has been added successfully!')
            return redirect('book-detail', pk=book.pk)
    else:
        return HttpResponseNotFound("Method is not supported")


def book_list(request):
    """
    Shows page with a list of books in the library.
    """
    book_list = Book.objects.all().order_by('title')
    paginator = Paginator(book_list, 8)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return TemplateResponse(request, 'book_list.html', {
        "page_obj": page_obj
    })

def book_search(request):
    books = []
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__name__icontains=query)
        )
    return TemplateResponse(request, 'book_search_results.html',{
        "books": books
    })