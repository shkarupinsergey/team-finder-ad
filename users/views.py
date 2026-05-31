from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .models import User
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, CustomPasswordChangeForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('projects:list')
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('projects:list')
    else:
        form = CustomAuthenticationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'users/login.html', context)


@login_required
def user_logout(request):
    logout(request)
    return redirect('users:login')


@login_required
def user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {
        'user': user,
    }
    return render(request, 'users/user-details.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:details', user_id=request.user.id)
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'users/edit_profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:details', user_id=request.user.id)
    else:
        form = CustomPasswordChangeForm(request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'users/change_password.html', context)


def participants_list(request):
    users = User.objects.all()
    context = {
        'participants': users,
    }
    return render(request, 'users/participants.html', context)
