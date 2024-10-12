from warnings import catch_warnings

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
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
        rating = None
        user_book_form = UserBookForm()
        user_book_interaction = None

        if request.user.is_authenticated and request.user.profile.is_read(book):
            user_book_interaction = UserBookInteraction.get_or_none(profile=request.user.profile, book=book)
            allow_add = False
            rating = UserBookInteraction.get_rating_or_none(profile=request.user.profile, book=book)
            user_book_form = UserBookForm(instance=user_book_interaction)

        return TemplateResponse(request, "single_book.html", {
            "book": book,
            "allow_add": allow_add,
            "rating": rating,
            "form": user_book_form,
            "user_interaction": user_book_interaction,
            "is_authenticated": request.user.is_authenticated,
        })
    elif request.method == 'POST' and request.user.is_authenticated:
        profile = request.user.profile
        if 'book_id' in request.POST:
            profile.add_book(book)
        elif 'book_id_review' in request.POST:
            user_book_interaction = UserBookInteraction.objects.get_or_create(profile=request.user.profile, book=book )[0]
            form = UserBookForm(request.POST, instance=user_book_interaction)
            if form.is_valid():
                review = form.save(commit=False)
                review.profile= profile
                review.book = book
                review.save()
                return TemplateResponse(request, 'single_book.html',
                                        { 'form': form,
                                        'profile': profile,
                                          'book': book,
                                          "is_authenticated": request.user.is_authenticated,
                })
            else:
                form = UserBookForm(instance=user_book_interaction)
                return TemplateResponse(request, "single_book.html", {
                    "book": book,
                    "form": form,
                    "is_authenticated": request.user.is_authenticated,
                })
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