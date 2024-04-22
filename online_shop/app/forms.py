from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Product, UserProfile, Comment, Message


# class LoginForm(AuthenticationForm):
#     username = forms.CharField(max_length=100)
#     password = forms.CharField(widget=forms.PasswordInput)


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))


class UserSignupForm(UserCreationForm):
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError(_('Parol kamida 8 ta belgidan iborat bo\'lishi kerak.'))
        return password1

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'img', 'name', 'price', 'description']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', 'email', 'img', 'address', 'phone', 'mobile']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
