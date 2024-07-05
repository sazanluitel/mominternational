from django.contrib import admin
from django.urls import path
from events.views import *

app_name="events"

urlpatterns = [
    path("",FrontPage.as_view(), name='frontpage'),
]
