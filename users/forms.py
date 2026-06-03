from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)

from .models import User

NAME_MAX_LENGTH = 100


class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=NAME_MAX_LENGTH, required=True)
    surname = forms.CharField(max_length=NAME_MAX_LENGTH, required=True)

    class Meta:
        model = User
        fields = ("name", "surname", "email", "password1", "password2")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
            "surname": forms.TextInput(attrs={"class": "form-input"}),
            "email": forms.EmailInput(attrs={"class": "form-input"}),
            "password1": forms.PasswordInput(attrs={"class": "form-input"}),
            "password2": forms.PasswordInput(attrs={"class": "form-input"}),
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-input"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-input"})
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "surname", "about", "phone", "github_url", "avatar"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
            "surname": forms.TextInput(attrs={"class": "form-input"}),
            "about": forms.Textarea(attrs={"class": "form-input", "rows": 4}),
            "phone": forms.TextInput(attrs={"class": "form-input"}),
            "github_url": forms.URLInput(attrs={"class": "form-input"}),
            "avatar": forms.FileInput(attrs={"class": "form-input"}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-input"}),
        label="Текущий пароль",
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-input"}), label="Новый пароль"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-input"}),
        label="Подтвердите новый пароль",
    )
