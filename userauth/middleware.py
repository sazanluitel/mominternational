from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from events import views

class AccessCheck:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path_info.startswith('/admin'):
            if not request.user.is_authenticated:
                return redirect('userauth:login')  # Adjust the login URL as necessary
            if not request.user.is_staff:
                return redirect('events:frontpage')
        
        response = self.get_response(request)
        return response
