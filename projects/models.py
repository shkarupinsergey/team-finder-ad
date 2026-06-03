from django.conf import settings
from django.db import models

SKILL_NAME_MAX_LENGTH = 100
PROJECT_NAME_MAX_LENGTH = 200
PROJECT_STATUS_MAX_LENGTH = 20
PROJECT_STATUS_OPEN = "open"
PROJECT_STATUS_CLOSED = "closed"


class Skill(models.Model):
    name = models.CharField(max_length=SKILL_NAME_MAX_LENGTH, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        (PROJECT_STATUS_OPEN, "Открыт"),
        (PROJECT_STATUS_CLOSED, "Закрыт"),
    ]

    name = models.CharField(max_length=PROJECT_NAME_MAX_LENGTH)
    description = models.TextField()
    github_url = models.URLField(blank=True, null=True)
    status = models.CharField(
        max_length=PROJECT_STATUS_MAX_LENGTH,
        choices=STATUS_CHOICES,
        default=PROJECT_STATUS_OPEN,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participating_projects",
        blank=True,
    )
    skills = models.ManyToManyField(Skill, related_name="projects", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name


class FavoriteProject(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorite_projects",
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "project")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user.username} - {self.project.name}"
