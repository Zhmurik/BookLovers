from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm, CustomUserLoginForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def LoginView(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Используйте имя URL, а не HTML файл
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = CustomUserLoginForm()

    return render(request, 'login.html', {'form': form})


def LogoutView(request):
    logout(request)
    return render(request, 'logout.html')


