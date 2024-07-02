from django.db import models
import uuid
from django.utils import timezone

STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived'),
]

class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique = True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)