from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from ..models import Author


def author_list(request):
    """
        Shows page with author list.
    """
    authors = Author.objects.all()
    return TemplateResponse(request, "author_list.html", {
        'authors': authors
    })


def author_detail(request, author_id):
    """
        Shows page with information about the author.
    """
    author = get_object_or_404(Author, id=author_id)
    return TemplateResponse(request, "author_detail.html", {
        'author': author
    })