from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseNotFound
from django.template.response import TemplateResponse

from ..forms import UserBookForm
from ..models import Book, UserBookInteraction


@login_required
def profile(request):
    """
        Displaying page with information about the user and his read books.
    """
    profile = request.user.profile
    books = profile.read_books.all()
    return TemplateResponse(request, "profile.html",{
        "profile": profile,
        "read_books": books
    })

def add_notes(request, pk):
    book = Book.objects.get(pk=pk)

    if request.method == "GET":
        return TemplateResponse(request, 'single_book_form_notes.html',
                                    {'book': book, 'form': UserBookForm()})
    if request.method == "POST":
        user_book_interaction = UserBookInteraction.objects.get_or_create(profile=request.user.profile, book=book)[0]
        form = UserBookForm(request.POST, instance=user_book_interaction)

        profile = request.user.profile
        if form.is_valid():
            review = form.save(commit=False)
            review.profile = profile
            review.book = book
            review.save()
            messages.success(request, 'The book has been added successfully!')
            books = profile.read_books.all()
            return TemplateResponse(request, 'profile.html',
                                    {'read_books': books, 'profile':review.profile})
        else:
            return HttpResponseNotFound("Form data is invalid")

    else:
        return HttpResponseNotFound("Method is not supported")