from django.contrib.auth.models import AbstractUser
from django.db import models

NAME_MAX_LENGTH = 100
PHONE_MAX_LENGTH = 20


class User(AbstractUser):
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    surname = models.CharField(max_length=NAME_MAX_LENGTH)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=PHONE_MAX_LENGTH, blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ("email",)

    def __str__(self):
        return f"{self.name} {self.surname}"
