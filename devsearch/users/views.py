from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required


# Create your views here.


def loginUser(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username, password=password)
        except:
            messages.error(request, "User does'not exist")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("profiles")
        else:
            messages.error(request, "Username or password incorrect!")
    return render(request, "users/login_register.html")


def logoutUser(request):
    logout(request)
    messages.info(request, "User successfully logged out")
    return redirect("login")


def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # To get form instance and edit it, reger below
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User successfully registered")
            login(request, user)
            return redirect("profiles")
        else:
            messages.success(request, "An error has occured during registration")

    context = {"page": page, "form": form}
    return render(request, "users/login_register.html", context)


def profiles(request):
    profiles = Profile.objects.all()
    context = {"profiles": profiles}
    return render(request, "users/profiles.html", context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topskills = profile.skill_set.exclude(description__exact="")
    otherskills = profile.skill_set.filter(description="")
    context = {"profile": profile, "topskills": topskills, "otherskills": otherskills}
    return render(request, "users/user-profile.html", context)


@login_required(login_url="login")
def userAccount(request):
    # (request.user) will give us the current logged in user information
    # (request.user.profile) will give us the current logged in user profile
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()  # to fetch child model info from parent model
    context = {"profile": profile, "skills": skills, "projects": projects}
    return render(request, "users/account.html", context)
