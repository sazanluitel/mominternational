from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomUserCreationForm, UserLoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(View):
    def post(self, request):
        form = CustomUserCreationForm(data=request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                "success": True,
                "message": "User created successfully."
            })
        return JsonResponse({
            "success": False,
            "errors": form.errors.as_json()
        }, status=500)

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

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
