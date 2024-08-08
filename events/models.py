from django.db import models
from momsinternational.basemodel import BaseModel

# Create your models here.

class Events(BaseModel, models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    entry_charge = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.title
