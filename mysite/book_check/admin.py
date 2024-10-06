from django.contrib import admin

from .models import Book, Profile, Author, Rating, Tag, UserBookInteraction


class BookInline(admin.TabularInline):
    model = Book
    extra = 1


class UserBookInline(admin.TabularInline):
    model = UserBookInteraction
    extra = 1


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth', 'date_of_death')
    search_fields = ('name',)
    list_filter = ('date_of_birth', 'date_of_death')
    inlines = [BookInline]


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'get_genre_display',
                    'description', 'cover_image')
    search_fields = ('title', 'author__name')
    list_filter = ('genres', 'published_date')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    inlines = [UserBookInline]


class UserBookAdmin(admin.ModelAdmin):
    list_display = ('profile', 'book', 'note')
    search_fields = ('user_profile__user__username', 'book__title', 'note')
    list_filter = ('book__genres',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_name',)
    search_fields = ('tag_name',)


admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(UserBookInteraction, UserBookAdmin)
