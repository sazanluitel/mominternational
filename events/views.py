from django.shortcuts import render
from django.views import View


def FrontPage(request):
    return render(request, 'index.html')
