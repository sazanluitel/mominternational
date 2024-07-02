from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth import authenticate

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'fullname', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        return email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise ValidationError("Invalid email or password")
            self.user = user

    def get_user(self):
        return getattr(self, 'user', None)
