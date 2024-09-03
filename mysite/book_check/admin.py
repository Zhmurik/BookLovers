from django.contrib import admin

from .models import Book, Profile, Author,Rating


class BookInline(admin.TabularInline):
    model = Book
    extra = 1


class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]


admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Rating)
