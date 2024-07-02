from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.FrontPage, name= 'front_page'),
]
