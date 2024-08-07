from django.db import models
from momsinternational.basemodel import BaseModel


# Create your models here.

class Events(BaseModel, models.Model):
    title = models.CharField(max_length=100)
    no_of_people = models.IntegerField(default=0)
    category = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
    
