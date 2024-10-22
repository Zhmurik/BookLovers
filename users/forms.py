from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'plaseholder': 'Enter your username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Create password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Re-type your password'})

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomUserLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label='Remember Me')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CustomUserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter your username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter your password'})

    def clean(self):
        cleaned_data = super().clean()
        user = self.get_user()
        if user is not None and self.request is not None:
            login(self.request, user)
            remember_me = cleaned_data.get('remember_me')
            if remember_me:
                self.request.session.set_expiry(1209600)
            else:
                self.request.session.set_expiry(0)

        return cleaned_data
