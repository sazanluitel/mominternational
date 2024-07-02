from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    #AbstractUser handles all the fields like password1, password2, first_name, last_name etc
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    def save(self, *args, **kwargs):
        self.email = self.email.lower()  # Normalize email to lowercase
        super().save(*args, **kwargs)
