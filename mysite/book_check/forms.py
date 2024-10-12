from django import forms

from .models import UserBookInteraction


class UserBookForm(forms.ModelForm):
    class Meta:
        model = UserBookInteraction
        fields = ['rating', 'tags', 'note']

        widgets = {
            'tags': forms.TextInput(attrs={'placeholder': 'Enter tags'}),
            'rating': forms.Select(choices=[
                (1, '1 - Poor'),
                (2, '2 - Fair'),
                (3, '3 - Good'),
                (4, '4 - Very Good'),
                (5, '5 - Excellent'),
            ]),
            'note': forms.Textarea(attrs={'placeholder': 'Enter your notes'}),
        }
