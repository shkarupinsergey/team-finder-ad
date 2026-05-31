from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
