from django.contrib import admin
from django.urls import path
from .views import FrontPage, AboutPage, ContactPage

app_name = "events"

urlpatterns = [
    path("", FrontPage.as_view(), name='front_page'),
    path("about/", AboutPage.as_view(), name='about_page'),
    path("contact/", ContactPage.as_view(), name='contact_page'),
]
