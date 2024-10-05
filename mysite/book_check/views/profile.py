from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse


@login_required(login_url='login/')
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