from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("USER", "User"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="USER")

    def is_admin(self):
        return self.role == "ADMIN" or self.is_staff or self.is_superuser

    def __str__(self):
        return self.username
