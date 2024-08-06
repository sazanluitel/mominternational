from django.contrib import admin
from django.urls import path
from .views import FrontPage, AboutPage, ContactPage

app_name = "events"

urlpatterns = [
    path("", FrontPage.as_view(), name='frontpage'),
    path("about/", AboutPage.as_view(), name='aboutpage'),
    path("contact/", ContactPage.as_view(), name='contactpage'),
]
