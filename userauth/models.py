from django.db import models
from django.contrib.auth.models import AbstractUser
from momsinternational.settings import STATIC_URL


class User(AbstractUser):
    email = models.EmailField(unique=True)
    image= models.TextField(blank=True, null=True )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        # If username is not provided, generate it from email
        if not self.username and self.email:
            base_username = self.email.split('@')[0]
            unique_username = base_username #suresh
            counter = 1

            # Ensure the generated username is unique
            while User.objects.filter(username=unique_username).exists():
                unique_username = f"{base_username}_{counter}"
                counter += 1

            self.username = unique_username
        super().save(*args, **kwargs)

    def get_avatar(self) -> str:
        if self.image:
            return self.image
        return "/" + STATIC_URL +  "assets/images/user.png"
    
    def get_full_name(self):
        # Assuming your model has fields 'first_name' and 'last_name'
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return "Anonymous"
    
    def get_role(self):
        # Assuming your model has a field 'role'
        return self.role.capitalize()