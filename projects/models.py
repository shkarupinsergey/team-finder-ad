from django.db import models
from django.conf import settings


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ('open', 'Открыт'),
        ('closed', 'Закрыт'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    github_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_projects')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participating_projects', blank=True)
    skills = models.ManyToManyField(Skill, related_name='projects', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FavoriteProject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_projects')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.username} - {self.project.name}"
