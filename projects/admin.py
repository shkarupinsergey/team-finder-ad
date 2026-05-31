from django.contrib import admin
from .models import Project, Skill, FavoriteProject


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['skills', 'participants']


@admin.register(FavoriteProject)
class FavoriteProjectAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'created_at']
    list_filter = ['created_at']
