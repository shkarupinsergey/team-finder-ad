from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import ProjectForm
from .models import (
    FavoriteProject,
    PROJECT_STATUS_CLOSED,
    PROJECT_STATUS_OPEN,
    Project,
    Skill,
)

SKILL_SUGGESTIONS_LIMIT = 10


def project_list(request):
    skill_filter = request.GET.get("skill")
    projects = (
        Project.objects.filter(status=PROJECT_STATUS_OPEN)
        .select_related("owner")
        .prefetch_related("skills", "participants")
    )

    if skill_filter:
        projects = projects.filter(skills__name=skill_filter)

    all_skills = Skill.objects.all()
    active_skill = skill_filter

    context = {
        "projects": projects,
        "all_skills": all_skills,
        "active_skill": active_skill,
    }
    return render(request, "projects/project_list.html", context)


def project_details(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    context = {
        "project": project,
    }
    return render(request, "projects/project-details.html", context)


@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect("projects:details", project_id=project.id)
    else:
        form = ProjectForm()

    context = {
        "form": form,
        "is_edit": False,
    }
    return render(request, "projects/create-project.html", context)


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects:details", project_id=project.id)
    else:
        form = ProjectForm(instance=project)

    context = {
        "form": form,
        "is_edit": True,
        "project": project,
    }
    return render(request, "projects/create-project.html", context)


@login_required
def favorite_projects(request):
    if not request.user.is_authenticated:
        return redirect("users:login")

    favorite_project_ids = FavoriteProject.objects.filter(
        user=request.user
    ).values_list("project_id", flat=True)
    projects = (
        Project.objects.filter(id__in=favorite_project_ids)
        .select_related("owner")
        .prefetch_related("skills", "participants")
    )

    context = {
        "projects": projects,
    }
    return render(request, "projects/favorite_projects.html", context)


@login_required
def toggle_favorite(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        project = Project.objects.filter(pk=project_id).first()

        if project is None:
            return JsonResponse(
                {"error": "Project not found"},
                status=HTTPStatus.NOT_FOUND,
            )

        favorite, created = FavoriteProject.objects.get_or_create(
            user=request.user,
            project=project,
        )

        if not created:
            favorite.delete()
            is_favorited = False
        else:
            is_favorited = True

        return JsonResponse({"is_favorited": is_favorited})

    return JsonResponse(
        {"error": "Invalid request"},
        status=HTTPStatus.BAD_REQUEST,
    )


@login_required
def toggle_participation(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        project = Project.objects.filter(pk=project_id).first()

        if project is None:
            return JsonResponse(
                {"error": "Project not found"},
                status=HTTPStatus.NOT_FOUND,
            )

        participant = project.participants.filter(pk=request.user.pk).first()
        if participant is not None:
            project.participants.remove(request.user)
            is_participating = False
        else:
            project.participants.add(request.user)
            is_participating = True

        return JsonResponse({"is_participating": is_participating})

    return JsonResponse(
        {"error": "Invalid request"},
        status=HTTPStatus.BAD_REQUEST,
    )


@login_required
def complete_project(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        project = Project.objects.filter(pk=project_id, owner=request.user).first()

        if project is None:
            return JsonResponse(
                {"error": "Project not found"},
                status=HTTPStatus.NOT_FOUND,
            )

        project.status = PROJECT_STATUS_CLOSED
        project.save()
        return JsonResponse({"success": True})

    return JsonResponse(
        {"error": "Invalid request"},
        status=HTTPStatus.BAD_REQUEST,
    )


@login_required
def add_skill(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        skill_name = request.POST.get("skill_name")
        project = Project.objects.filter(pk=project_id, owner=request.user).first()

        if project is None:
            return JsonResponse(
                {"error": "Project not found"},
                status=HTTPStatus.NOT_FOUND,
            )

        skill, created = Skill.objects.get_or_create(name=skill_name)
        project.skills.add(skill)

        return JsonResponse({"skill_id": skill.id, "skill_name": skill.name})

    return JsonResponse(
        {"error": "Invalid request"},
        status=HTTPStatus.BAD_REQUEST,
    )


@login_required
def remove_skill(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        skill_id = request.POST.get("skill_id")
        project = Project.objects.filter(pk=project_id, owner=request.user).first()
        skill = Skill.objects.filter(pk=skill_id).first()

        if project is None:
            return JsonResponse(
                {"error": "Project not found"},
                status=HTTPStatus.NOT_FOUND,
            )

        if skill is None:
            return JsonResponse(
                {"error": "Skill not found"},
                status=HTTPStatus.NOT_FOUND,
            )

        project.skills.remove(skill)
        return JsonResponse({"success": True})

    return JsonResponse(
        {"error": "Invalid request"},
        status=HTTPStatus.BAD_REQUEST,
    )


def skill_suggestions(request):
    query = request.GET.get("q", "")
    skills = Skill.objects.filter(name__icontains=query)[:SKILL_SUGGESTIONS_LIMIT]
    suggestions = [{"id": skill.id, "name": skill.name} for skill in skills]
    return JsonResponse({"suggestions": suggestions})
