from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from ..models import Book


def single_book(request, pk):
    """
        Shows page with a single book in the library.
    """
    book = get_object_or_404(Book, pk=pk)
    # if self.request.user.is_authenticated:
    #     user_profile_id = self.request.user.id
    #     user_book = UserBook.objects.get(user_profile_id=user_profile_id, book_id=book_id)
    #     context['book_to_rating'] = user_book.rating
    #     context['notes'] = user_book.note
    #     context['tags'] = user_book.tags
    return TemplateResponse( request, "single_book.html", {
        "book": book,
    })

def book_list(request):
    """
    Shows page with a list of books in the library.
    """
    book_list = Book.objects.all().order_by('title')
    paginator = Paginator(book_list, 8)

    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        books = paginator.page(1)
    except EmptyPage:
        # If the page is out of range (e.g., 9999), deliver the last page of results.
        books = paginator.page(paginator.num_pages)
    return TemplateResponse(request, 'book_list.html', {
        "books": books
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