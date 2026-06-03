from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("list/", views.project_list, name="list"),
    path("<int:project_id>/", views.project_details, name="details"),
    path("create-project/", views.create_project, name="create"),
    path("<int:project_id>/edit/", views.edit_project, name="edit"),
    path("favorites/", views.favorite_projects, name="favorites"),
    path("toggle-favorite/", views.toggle_favorite, name="toggle_favorite"),
    path(
        "toggle-participation/", views.toggle_participation, name="toggle_participation"
    ),
    path("complete-project/", views.complete_project, name="complete"),
    path("add-skill/", views.add_skill, name="add_skill"),
    path("remove-skill/", views.remove_skill, name="remove_skill"),
    path("skill-suggestions/", views.skill_suggestions, name="skill_suggestions"),
]
