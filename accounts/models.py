from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.


class CustomUser(AbstractUser):
    picture = models.ImageField(null=True)
    phone_number = models.CharField(
        null=True, max_length=10, help_text="must be 10 characters long"
    )
    last_seen = models.DateTimeField(default=timezone.now)

    class Meta(AbstractUser.Meta):
        ordering = ("username", "pk")

    def __str__(self):
        return self.username

    
        

    
