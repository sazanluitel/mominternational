from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomUserCreationForm, UserLoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
class RegisterView(View):
    def post(self, request):
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please log in to continue.')
            return redirect('login')
        return render(request, 'signup.html', {'form': form})

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form})

class LoginView(View):
    def post(self, request):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid email or password')
        return render(request, 'login.html', {'form': form})

    def get(self, request):
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})
