from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('book_check.urls')),
    path('', include('users.urls')),

]
